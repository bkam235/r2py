# r2py crawler metadata
# package: yaml
# source_type: rd_example
# topic: verbatim_logical.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\yaml\help
# lines: 4

suppressPackageStartupMessages(library(yaml))
vector <- c(TRUE, FALSE, TRUE)

as.yaml(vector, handlers=list(logical=verbatim_logical))