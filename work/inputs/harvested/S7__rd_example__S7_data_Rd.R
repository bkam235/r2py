# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: S7_data.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 8

suppressPackageStartupMessages(library(S7))
Text <- new_class("Text", parent = class_character)
y <- Text(c(foo = "bar"))
y
S7_data(y)

S7_data(y) <- c("a", "b")
y