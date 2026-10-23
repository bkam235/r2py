# r2py crawler metadata
# package: vroom
# source_type: vignette
# topic: vroom_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\doc\vroom.R
# lines: 7

suppressPackageStartupMessages(library(vroom))
zip_file <- vroom_example("mtcars-multi-cyl.zip")
filenames <- unzip(zip_file, list = TRUE)$Name
filenames

# imagine we only want to read 2 of the 3 files
vroom(purrr::map(filenames[c(1, 3)], \(x) unz(zip_file, x)))