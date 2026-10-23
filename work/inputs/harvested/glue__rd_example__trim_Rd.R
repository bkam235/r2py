# r2py crawler metadata
# package: glue
# source_type: rd_example
# topic: trim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\help
# lines: 16

suppressPackageStartupMessages(library(glue))
glue("
    A formatted string
    Can have multiple lines
      with additional indention preserved
    ")

glue("
  \ntrailing or leading newlines can be added explicitly\n
  ")

glue("
    A formatted string \\
    can also be on a \\
    single line
    ")