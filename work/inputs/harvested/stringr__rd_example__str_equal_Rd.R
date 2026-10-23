# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: str_equal.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 17

suppressPackageStartupMessages(library(stringr))
# These two strings encode "a" with an accent in two different ways
a1 <- "\u00e1"
a2 <- "a\u0301"
c(a1, a2)

a1 == a2
str_equal(a1, a2)

# ohm and omega use different code points but should always be treated
# as equal
ohm <- "\u2126"
omega <- "\u03A9"
c(ohm, omega)

ohm == omega
str_equal(ohm, omega)