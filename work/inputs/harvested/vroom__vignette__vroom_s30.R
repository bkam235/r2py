# r2py crawler metadata
# package: vroom
# source_type: vignette
# topic: vroom_s30
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\doc\vroom.R
# lines: 6

suppressPackageStartupMessages(library(vroom))
vroom_write(mtcars, "mtcars.tsv.gz")

vroom_write(mtcars, "mtcars.tsv.bz2")

vroom_write(mtcars, "mtcars.tsv.xz")