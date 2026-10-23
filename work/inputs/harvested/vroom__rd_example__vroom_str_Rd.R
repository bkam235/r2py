# r2py crawler metadata
# package: vroom
# source_type: rd_example
# topic: vroom_str.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\help
# lines: 6

suppressPackageStartupMessages(library(vroom))
# when used on non-altrep objects altrep will always be false
vroom_str(mtcars)

mt <- vroom(vroom_example("mtcars.csv"), ",", altrep = c("chr", "dbl"))
vroom_str(mt)