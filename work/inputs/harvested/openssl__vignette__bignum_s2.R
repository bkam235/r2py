# r2py crawler metadata
# package: openssl
# source_type: vignette
# topic: bignum_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\doc\bignum.R
# lines: 14

suppressPackageStartupMessages(library(openssl))
# create a bignum
y <- bignum("123456789123456789")
z <- bignum("D41D8CD98F00B204E9800998ECF8427E", hex = TRUE)

# size grows
print(y * z)

# Basic arithmetic
div <- z %/% y
mod <- z %% y
z2 <- div * y + mod
stopifnot(z2 == z)
stopifnot(div < z)