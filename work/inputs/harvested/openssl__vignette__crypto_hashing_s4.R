# r2py crawler metadata
# package: openssl
# source_type: vignette
# topic: crypto_hashing_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\doc\crypto_hashing.R
# lines: 4

suppressPackageStartupMessages(library(openssl))
# Stream-hash a file
myfile <- system.file("CITATION")
md5(file(myfile))