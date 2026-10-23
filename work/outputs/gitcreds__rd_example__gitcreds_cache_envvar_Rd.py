# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import re
from urllib.parse import urlparse

# r2py:entity:gitcreds_cache_envvar
def gitcreds_cache_envvar(url):
    parsed = urlparse(url)
    protocol = parsed.scheme
    host = parsed.hostname
    username = parsed.username if parsed.username else ""

    if not protocol or not host:
        raise ValueError(f"Invalid URL(s): {url}")

    # proto <- sub("^https?_$", "", paste0(pcs$protocol, "_"))
    proto_val = f"{protocol}_"
    proto_val = re.sub(r"^https?_$", "", proto_val)

    # user <- ifelse(pcs$username != "", paste0(pcs$username, "_AT_"), "")
    user_val = f"{username}_AT_" if username != "" else ""

    # host0 <- sub("^api[.]github[.]com$", "github.com", pcs$host)
    host0 = re.sub(r"^api\.github\.com$", "github.com", host)
    
    # host1 <- gsub("[.:]+", "_", host0)
    host1 = re.sub(r"[.:]+", "_", host0)
    
    # host <- gsub("[^a-zA-Z0-9_-]", "x", host1)
    host_val = re.sub(r"[^a-zA-Z0-9_-]", "x", host1)
    
    # slug1 <- paste0(proto, user, host)
    slug1 = f"{proto_val}{user_val}{host_val}"
    
    # slug2 <- ifelse(grepl("^AT_", slug1), paste0("AT_", slug1), slug1)
    slug2 = f"AT_{slug1}" if slug1.startswith("AT_") else slug1
    
    # slug3 <- ifelse(grepl("^[0-9]", slug2), paste0("AT_", slug2), slug2)
    slug3 = f"AT_{slug2}" if slug2 and slug2[0].isdigit() else slug2
    
    return f"GITHUB_PAT_{slug3.upper()}"

# r2py:entity:gitcreds_cache_envvar
print(gitcreds_cache_envvar("https://github.com"))
# r2py:entity:gitcreds_cache_envvar_1
print(gitcreds_cache_envvar("https://api.github.com/path/to/endpoint"))
# r2py:entity:gitcreds_cache_envvar_2
print(gitcreds_cache_envvar("https://jane@github.com"))
# r2py:entity:gitcreds_cache_envvar_3
print(gitcreds_cache_envvar("https://another.site.github.com"))