# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: recipes_ptype_validate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 4

suppressPackageStartupMessages(library(recipes))
rec <- recipe(mpg ~ disp, data = mtcars)

recipes_ptype_validate(rec, mtcars)