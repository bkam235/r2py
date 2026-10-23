# r2py crawler metadata
# package: vroom
# source_type: vignette
# topic: vroom_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\doc\vroom.R
# lines: 9

suppressPackageStartupMessages(library(vroom))
# read the 'hp' columns as an integer
vroom(vroom_example("mtcars.csv"), col_types = c(hp = "i"))

# also skip reading the 'cyl' column
vroom(vroom_example("mtcars.csv"), col_types = c(hp = "i", cyl = "_"))

# also read the gears as a factor
vroom(vroom_example("mtcars.csv"), col_types = c(hp = "i", cyl = "_", gear = "f"))