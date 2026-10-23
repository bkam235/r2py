# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s31
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 8

suppressPackageStartupMessages(library(xtable))
dat <- mtcars[1:3, 1:6]
large <- function(x){
  paste0('{\\Large{\\bfseries ', x, '}}')
}
italic <- function(x){
  paste0('{\\emph{ ', x, '}}')
}