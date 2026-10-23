# r2py crawler metadata
# package: curl
# source_type: rd_example
# topic: handle_cookies.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\help
# lines: 15

suppressPackageStartupMessages(library(curl))
h <- new_handle()
handle_cookies(h)

# Server sets cookies
req <- curl_fetch_memory("https://hb.cran.dev/cookies/set?foo=123&bar=ftw", handle = h)
handle_cookies(h)

# Server deletes cookies
req <- curl_fetch_memory("https://hb.cran.dev/cookies/delete?foo", handle = h)
handle_cookies(h)

# Cookies will survive a reset!
handle_reset(h)
handle_cookies(h)