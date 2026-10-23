# r2py crawler metadata
# package: R6
# source_type: rd_example
# topic: is.R6.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\R6\help
# lines: 9

suppressPackageStartupMessages(library(R6))
class_generator <- R6Class()
object <- class_generator$new()

is.R6Class(class_generator)
is.R6(class_generator)

is.R6Class(object)
is.R6(object)