# r2py crawler metadata
# package: glue
# source_type: rd_example
# topic: glue_collapse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\help
# lines: 7

suppressPackageStartupMessages(library(glue))
glue_collapse(glue("{1:10}"))

# Wide values can be truncated
glue_collapse(glue("{1:10}"), width = 5)

glue_collapse(1:4, ", ", last = " and ")