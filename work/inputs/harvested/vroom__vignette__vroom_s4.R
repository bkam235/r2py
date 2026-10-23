# r2py crawler metadata
# package: vroom
# source_type: vignette
# topic: vroom_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\doc\vroom.R
# lines: 4

suppressPackageStartupMessages(library(vroom))
ve <- grep("mtcars-[0-9].csv", vroom_examples(), value = TRUE)
files <- sapply(ve, vroom_example)
files