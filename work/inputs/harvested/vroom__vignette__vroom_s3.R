# r2py crawler metadata
# package: vroom
# source_type: vignette
# topic: vroom_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\doc\vroom.R
# lines: 11

suppressPackageStartupMessages(library(vroom))
# See where the example file is stored on your machine
file <- vroom_example("mtcars.csv")
file

# Read the file, by default vroom will guess the delimiter automatically.
vroom(file)

# You can also specify it explicitly, which is (slightly) faster, and safer if
# you know how the file is delimited.
vroom(file, delim = ",")