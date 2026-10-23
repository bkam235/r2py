# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 8

suppressPackageStartupMessages(library(curl))
try({
# URLOPT_MASFILESIZE must be a number
handle_setopt(handle, maxfilesize = "foo")

# CURLOPT_USERAGENT must be a string
handle_setopt(handle, useragent = 12345)
})