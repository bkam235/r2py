# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s22
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 21

suppressPackageStartupMessages(library(xtable))
italic <- function(x){
  paste0('{\\emph{', x, '}}')
}
mtcars$cyl <- factor(mtcars$cyl, levels = c("four","six","eight"),
                     labels = c("four",italic("six"),"eight"))
large <- function(x){
  paste0('{\\Large ', x, '}')
}
bold <- function(x){
  paste0('{\\bfseries ', x, '}')
}
tbl <- ftable(mtcars$cyl, mtcars$vs, mtcars$am, mtcars$gear,
              row.vars = c(2, 4),
              dnn = c("Cylinders", "V/S", "Transmission", "Gears"))
xftbl <- xtableFtable(tbl, method = "row.compact")
print.xtableFtable(xftbl,
                   sanitize.rownames.function = large,
                   sanitize.colnames.function = bold,
                   rotate.colnames = TRUE,
                   rotate.rownames = TRUE)