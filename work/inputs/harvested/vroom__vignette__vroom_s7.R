# r2py crawler metadata
# package: vroom
# source_type: vignette
# topic: vroom_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\doc\vroom.R
# lines: 4

suppressPackageStartupMessages(library(vroom))
file <- vroom_example("mtcars.csv.gz")

vroom(file)