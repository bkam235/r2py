# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: tibble_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\tibble.R
# lines: 8

suppressPackageStartupMessages(library(tibble))
try({
df <- data.frame(abc = 1)
df$a

df2 <- tibble(abc = 1)
df2$a
})