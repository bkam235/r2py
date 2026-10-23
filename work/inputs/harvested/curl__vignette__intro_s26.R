# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s26
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 12

suppressPackageStartupMessages(library(curl))
# Start with a fresh handle
h <- new_handle()

# Ask server to set some cookies
req <- curl_fetch_memory("https://hb.cran.dev/cookies/set?foo=123&bar=ftw", handle = h)
req <- curl_fetch_memory("https://hb.cran.dev/cookies/set?baz=moooo", handle = h)
handle_cookies(h)

# Unset a cookie
req <- curl_fetch_memory("https://hb.cran.dev/cookies/delete?foo", handle = h)
handle_cookies(h)