# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: base_s20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\base.R
# lines: 5

suppressPackageStartupMessages(library(dplyr))
mtcars[union(c("gear", "carb"), names(mtcars))]

to_back <- c("mpg", "cyl")
mtcars[c(setdiff(names(mtcars), to_back), to_back)]