# r2py crawler metadata
# package: openssl
# source_type: vignette
# topic: crypto_hashing_chunk5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\doc\crypto_hashing.Rmd
# lines: 6

suppressPackageStartupMessages(library(openssl))
# Stream-hash from a network connection
as.character(md5(url("https://cran.r-project.org/bin/windows/base/old/4.0.0/R-4.0.0-win.exe")))

# Compare
readLines('https://cran.r-project.org/bin/windows/base/old/4.0.0/md5sum.txt')