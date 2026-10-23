# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: stability_s24
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\stability.R
# lines: 4

suppressPackageStartupMessages(library(vctrs))
df1 <- data.frame(x = 1)
df2 <- data.frame(x = 2)
str(c(df1, df1))