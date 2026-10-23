# r2py crawler metadata
# package: openssl
# source_type: vignette
# topic: crypto_hashing_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\doc\crypto_hashing.R
# lines: 8

suppressPackageStartupMessages(library(openssl))
# Compare to digest
library(digest)
digest("foo", "md5", serialize = FALSE)

# Other way around
digest(cars, skip = 0)
md5(serialize(cars, NULL))