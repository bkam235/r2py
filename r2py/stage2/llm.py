"""Stage 2 LLM client — Anthropic SDK with retry and prompt caching (§5)."""
from __future__ import annotations

import os
import time

import anthropic

_DEFAULT_MODEL = "claude-sonnet-4-6"
_MAX_RETRIES = 4

# Module-level client cache keyed by api_key so the underlying HTTP session
# is reused across all entity calls within a translation run.
_clients: dict[str, anthropic.Anthropic] = {}


def _get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Export it before running the translator."
        )
    if api_key not in _clients:
        _clients[api_key] = anthropic.Anthropic(api_key=api_key)
    return _clients[api_key]


def call(
    messages: list[dict],
    system: str,
    *,
    model: str = _DEFAULT_MODEL,
    max_tokens: int = 8192,
) -> str:
    """Call the Anthropic Messages API with exponential-backoff retry.

    The system prompt is sent with cache_control so it is cached after the first
    call in a run (all entity calls share the same static system prompt).

    Raises RuntimeError if ANTHROPIC_API_KEY is not set or the response is
    truncated (stop_reason == "max_tokens").
    """
    client = _get_client()

    # Wrap system as a list with cache_control so the prompt is cached.
    system_block = [
        {
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"},
        }
    ]

    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_block,
                messages=messages,
            )
            if response.stop_reason == "max_tokens":
                raise RuntimeError(
                    f"LLM response truncated at max_tokens={max_tokens}. "
                    "Increase max_tokens or reduce entity size."
                )
            return response.content[0].text
        except RuntimeError:
            raise  # truncation is deterministic — do not retry
        except (anthropic.RateLimitError, anthropic.APIConnectionError) as exc:
            last_exc = exc
            wait = 2 ** attempt  # 1, 2, 4, 8 s
            time.sleep(wait)
        except Exception:
            raise

    raise RuntimeError(f"LLM call failed after {_MAX_RETRIES} attempts: {last_exc}")
