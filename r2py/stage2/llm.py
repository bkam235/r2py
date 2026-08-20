"""Stage 2 LLM client — Anthropic SDK with retry and prompt caching (§5)."""
from __future__ import annotations

import os
import time

import anthropic

_DEFAULT_MODEL = "claude-sonnet-4-6"
_MAX_RETRIES = 4


class TruncatedResponseError(RuntimeError):
    """Raised when the LLM response was cut off at max_tokens."""
    def __init__(self, partial_text: str, max_tokens: int):
        self.partial_text = partial_text
        super().__init__(
            f"LLM response truncated at max_tokens={max_tokens}. "
            "Increase max_tokens or reduce entity size."
        )

# Module-level client cache keyed by api_key so the underlying HTTP session
# is reused across all entity calls within a translation run.
_clients: dict[str, anthropic.Anthropic] = {}
_ollama_clients: dict[str, object] = {}  # keyed by base_url; openai.OpenAI instances


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
    max_tokens: int = 16384,
) -> str:
    """Call the Anthropic Messages API with exponential-backoff retry.

    The system prompt is sent with cache_control so it is cached after the first
    call in a run (all entity calls share the same static system prompt).

    Raises RuntimeError if ANTHROPIC_API_KEY is not set or the response is
    truncated (stop_reason == "max_tokens").
    """
    if model.startswith("ollama:"):
        return _call_ollama(messages, system, model=model[len("ollama:"):], max_tokens=max_tokens)

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
                raise TruncatedResponseError(
                    response.content[0].text, max_tokens,
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


def _call_ollama(
    messages: list[dict],
    system: str,
    *,
    model: str,
    max_tokens: int,
) -> str:
    """Call a local Ollama model via its OpenAI-compatible endpoint."""
    try:
        import openai
    except ImportError:
        raise RuntimeError(
            "Ollama support requires the 'openai' package: pip install openai"
        )

    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434") + "/v1"
    if base_url not in _ollama_clients:
        _ollama_clients[base_url] = openai.OpenAI(api_key="ollama", base_url=base_url)
    client = _ollama_clients[base_url]

    all_messages = [{"role": "system", "content": system}] + messages

    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=all_messages,
                max_tokens=max_tokens,
            )
            finish_reason = response.choices[0].finish_reason
            if finish_reason == "length":
                usage = getattr(response, "usage", None)
                comp_tokens = getattr(usage, "completion_tokens", "?") if usage else "?"
                print(f"[LLM]     Warning: Ollama response truncated at {comp_tokens} tokens (max_tokens={max_tokens})")
            content = response.choices[0].message.content
            if content is None:
                raise RuntimeError(
                    f"Ollama returned null content "
                    f"(finish_reason={response.choices[0].finish_reason!r}). "
                    "The model may have emitted a tool call or an empty response."
                )
            return content
        except RuntimeError:
            raise  # deterministic errors — do not retry
        except Exception as exc:
            last_exc = exc
            wait = 2 ** attempt
            time.sleep(wait)

    raise RuntimeError(f"Ollama call failed after {_MAX_RETRIES} attempts: {last_exc}")
