"""Network call capture for R and Python sandboxes (§2.2 — Network/DB class).

Hooks are installed via preamble code injected before the user script.  Each
intercepted call appends a (verb, url, sha1_of_response) tuple to a module-level
log.  The epilogue serialises that log to _r2py_network.json.  collect() reads
the JSON and returns {"network_log": [...]}.

Supported:
  R    — httr::GET/POST/PUT/DELETE/PATCH, curl::curl_fetch_memory
  Python — requests.Session.request, urllib.request.urlopen
"""
from __future__ import annotations

import json
from pathlib import Path

# --------------------------------------------------------------------------- #
# R                                                                             #
# --------------------------------------------------------------------------- #

R_PREAMBLE = r"""
.r2py_net_log <- list()
local({
  .r2py_hash <- function(x) {
    if (is.raw(x)) {
      digest::digest(x, algo = "sha1", serialize = FALSE)
    } else {
      digest::digest(as.character(x)[1], algo = "sha1", serialize = FALSE)
    }
  }

  # Write directly to GlobalEnv so the epilogue (outside local()) can read it.
  .r2py_log_net <- function(verb, url, body_hash) {
    log <- get(".r2py_net_log", envir = .GlobalEnv)
    log[[length(log) + 1L]] <- list(verb, url, body_hash)
    assign(".r2py_net_log", log, envir = .GlobalEnv)
  }

  # Wrap httr verbs if httr is loaded
  if (requireNamespace("httr", quietly = TRUE)) {
    .r2py_orig_GET    <- httr::GET
    .r2py_orig_POST   <- httr::POST
    .r2py_orig_PUT    <- httr::PUT
    .r2py_orig_DELETE <- httr::DELETE
    .r2py_orig_PATCH  <- httr::PATCH

    r2py_GET <- function(url, ...) {
      r <- .r2py_orig_GET(url, ...)
      tryCatch(.r2py_log_net("GET", url, .r2py_hash(httr::content(r, "raw"))),
               error = function(e) NULL)
      r
    }
    r2py_POST <- function(url, ...) {
      r <- .r2py_orig_POST(url, ...)
      tryCatch(.r2py_log_net("POST", url, .r2py_hash(httr::content(r, "raw"))),
               error = function(e) NULL)
      r
    }
    r2py_PUT <- function(url, ...) {
      r <- .r2py_orig_PUT(url, ...)
      tryCatch(.r2py_log_net("PUT", url, .r2py_hash(httr::content(r, "raw"))),
               error = function(e) NULL)
      r
    }
    r2py_DELETE <- function(url, ...) {
      r <- .r2py_orig_DELETE(url, ...)
      tryCatch(.r2py_log_net("DELETE", url, .r2py_hash(httr::content(r, "raw"))),
               error = function(e) NULL)
      r
    }
    r2py_PATCH <- function(url, ...) {
      r <- .r2py_orig_PATCH(url, ...)
      tryCatch(.r2py_log_net("PATCH", url, .r2py_hash(httr::content(r, "raw"))),
               error = function(e) NULL)
      r
    }
    assign("GET",    r2py_GET,    envir = as.environment("package:httr"))
    assign("POST",   r2py_POST,   envir = as.environment("package:httr"))
    assign("PUT",    r2py_PUT,    envir = as.environment("package:httr"))
    assign("DELETE", r2py_DELETE, envir = as.environment("package:httr"))
    assign("PATCH",  r2py_PATCH,  envir = as.environment("package:httr"))
  }

  # Wrap curl::curl_fetch_memory if curl is loaded
  if (requireNamespace("curl", quietly = TRUE)) {
    .r2py_orig_cfm <- curl::curl_fetch_memory
    r2py_cfm <- function(url, ...) {
      r <- .r2py_orig_cfm(url, ...)
      tryCatch(.r2py_log_net("GET", url, .r2py_hash(r$content)),
               error = function(e) NULL)
      r
    }
    assign("curl_fetch_memory", r2py_cfm, envir = as.environment("package:curl"))
  }

})
"""

R_EPILOGUE = r"""
local({
  log <- get0(".r2py_net_log", envir = .GlobalEnv, inherits = FALSE)
  if (is.null(log)) log <- list()
  tryCatch({
    out <- if (requireNamespace("jsonlite", quietly = TRUE)) {
      jsonlite::toJSON(log, auto_unbox = TRUE)
    } else {
      "[]"
    }
    writeLines(as.character(out), "_r2py_network.json")
  }, error = function(e) writeLines("[]", "_r2py_network.json"))
})
"""

# --------------------------------------------------------------------------- #
# Python                                                                        #
# --------------------------------------------------------------------------- #

PY_PREAMBLE = r"""
import hashlib as _r2py_hashlib
_r2py_net_log = []

def _r2py_hash_bytes(b):
    if isinstance(b, (bytes, bytearray)):
        return _r2py_hashlib.sha1(b).hexdigest()
    return _r2py_hashlib.sha1(str(b).encode()).hexdigest()

try:
    import requests as _r2py_requests
    _r2py_orig_request = _r2py_requests.Session.request

    def _r2py_patched_request(self, method, url, **kwargs):
        resp = _r2py_orig_request(self, method, url, **kwargs)
        try:
            _r2py_net_log.append((method.upper(), url, _r2py_hash_bytes(resp.content)))
        except Exception:
            pass
        return resp

    _r2py_requests.Session.request = _r2py_patched_request
except ImportError:
    pass

try:
    import urllib.request as _r2py_urllib
    _r2py_orig_urlopen = _r2py_urllib.urlopen

    def _r2py_patched_urlopen(url, data=None, *args, **kwargs):
        resp = _r2py_orig_urlopen(url, data, *args, **kwargs)
        try:
            content = resp.read()
            _r2py_net_log.append(
                ("POST" if data else "GET",
                 getattr(url, "full_url", str(url)),
                 _r2py_hash_bytes(content))
            )
            # Wrap so caller can still read the body
            import io as _r2py_io
            import urllib.response as _r2py_ur
            return _r2py_ur.addinfourl(
                _r2py_io.BytesIO(content), resp.headers, resp.url, resp.status
            )
        except Exception:
            return resp

    _r2py_urllib.urlopen = _r2py_patched_urlopen
except Exception:
    pass
"""

PY_EPILOGUE = r"""
import json as _r2py_net_json
try:
    with open("_r2py_network.json", "w", encoding="utf-8") as _f:
        _r2py_net_json.dump(_r2py_net_log, _f)
except Exception:
    with open("_r2py_network.json", "w", encoding="utf-8") as _f:
        _f.write("[]")
"""

# --------------------------------------------------------------------------- #
# Collector                                                                     #
# --------------------------------------------------------------------------- #

def collect(workdir: Path) -> dict:
    """Read _r2py_network.json → {"network_log": [(verb, url, hash), ...]}."""
    path = workdir / "_r2py_network.json"
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return {}
        return {"network_log": [tuple(e) for e in raw if isinstance(e, list)]}
    except Exception:
        return {}
