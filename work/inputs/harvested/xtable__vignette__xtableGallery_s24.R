# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s24
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 5

suppressPackageStartupMessages(library(xtable))
data(mtcars)
dat <- mtcars[1:3, 1:6]
x <- xtable(dat)
x