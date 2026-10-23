# r2py crawler metadata
# package: glue
# source_type: vignette
# topic: glue_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\doc\glue.R
# lines: 6

suppressPackageStartupMessages(library(glue))
fn_def <- "
  <<NAME>> <- function(x) {
    # imagine a function body here
  }"
glue(fn_def, NAME = "my_function", .open = "<<", .close = ">>")