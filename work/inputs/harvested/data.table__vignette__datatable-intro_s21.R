# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-intro_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-intro.R
# lines: 8

suppressPackageStartupMessages(library(data.table))
DF = data.frame(x = c(1,1,1,2,2,3,3,3), y = 1:8)

## (1) normal way
DF[DF$x > 1, ] # data.frame needs that ',' as well

## (2) using with
DF[with(DF, x > 1), ]