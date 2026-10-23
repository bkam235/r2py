# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: prop.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 12

suppressPackageStartupMessages(library(S7))
Horse <- new_class("Horse", properties = list(
  name = class_character,
  colour = class_character,
  height = class_numeric
))
lexington <- Horse(colour = "bay", height = 15, name = "Lex")
lexington@colour
prop(lexington, "colour")

lexington@height <- 14
prop(lexington, "height") <- 15