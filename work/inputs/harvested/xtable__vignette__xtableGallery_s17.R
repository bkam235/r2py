# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 8

suppressPackageStartupMessages(library(xtable))
data(mtcars)
mtcars$cyl <- factor(mtcars$cyl, levels = c("4","6","8"),
                     labels = c("four","six","eight"))
tbl <- ftable(mtcars$cyl, mtcars$vs, mtcars$am, mtcars$gear,
              row.vars = c(2, 4),
              dnn = c("Cylinders", "V/S", "Transmission", "Gears"))
tbl