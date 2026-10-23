# r2py crawler metadata
# package: openssl
# source_type: vignette
# topic: secure_rng_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\doc\secure_rng.R
# lines: 4

suppressPackageStartupMessages(library(openssl))
# Secure rbinom
y <- qbinom(rand_num(1000), size = 20, prob = 0.1)
hist(y, breaks = -.5:(max(y)+1))