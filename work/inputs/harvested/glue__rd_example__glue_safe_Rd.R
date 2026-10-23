# r2py crawler metadata
# package: glue
# source_type: rd_example
# topic: glue_safe.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\help
# lines: 9

suppressPackageStartupMessages(library(glue))
"1 + 1" <- 5
# glue actually executes the code
glue("{1 + 1}")

# glue_safe just looks up the value
glue_safe("{1 + 1}")

rm("1 + 1")