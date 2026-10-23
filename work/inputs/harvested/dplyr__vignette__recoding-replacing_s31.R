# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: recoding-replacing_s31
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\recoding-replacing.R
# lines: 7

suppressPackageStartupMessages(library(dplyr))
x <- c(1, 2, 0, -99, 12)

# To convert `0` and `-99` to `NA`, you have to do it in two calls
x |> na_if(0) |> na_if(-99)

x |> replace_values(from = c(0, -99), to = NA)