# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: tibble_chunk12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\tibble.Rmd
# lines: 7

suppressPackageStartupMessages(library(tibble))
#| error: true
df <- data.frame(abc = 1)
df$a

df2 <- tibble(abc = 1)
df2$a