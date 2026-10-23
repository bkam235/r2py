# r2py crawler metadata
# package: openssl
# source_type: vignette
# topic: secure_rng_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\doc\secure_rng.R
# lines: 4

suppressPackageStartupMessages(library(openssl))
# Secure rnorm
x <- qnorm(rand_num(1000), mean = 100, sd = 15)
hist(x)