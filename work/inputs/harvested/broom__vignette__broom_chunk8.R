# r2py crawler metadata
# package: broom
# source_type: vignette
# topic: broom_chunk8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\doc\broom.Rmd
# lines: 4

suppressPackageStartupMessages(library(broom))
#| label: ttest
tt <- t.test(wt ~ am, mtcars)
tidy(tt)