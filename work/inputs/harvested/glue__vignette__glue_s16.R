# r2py crawler metadata
# package: glue
# source_type: vignette
# topic: glue_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\doc\glue.R
# lines: 7

suppressPackageStartupMessages(library(glue))
x <- "the local environment"
glue(
  "`glue()` can access values from {x} or from {y}. {z}",
  y = "named arguments",
  z = "Woo!"
)