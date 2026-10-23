# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: str_to_camel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 6

suppressPackageStartupMessages(library(stringr))
str_to_camel("my-variable")
str_to_camel("my-variable", first_upper = TRUE)

str_to_snake("MyVariable")
str_to_kebab("MyVariable")