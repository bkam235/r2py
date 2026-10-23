# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: listOfTablesGallery_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\listOfTablesGallery.R
# lines: 13

suppressPackageStartupMessages(library(xtable))
large <- function(x){
  paste0('{\\Large{\\bfseries ', x, '}}')
}
italic <- function(x){
  paste0('{\\emph{ ', x, '}}')
}
bold <- function(x){
  paste0('{\\bfseries ', x, '}')
}
red <- function(x){
  paste0('{\\color{red} ', x, '}')
}