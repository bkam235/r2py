# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: method-set.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 12

suppressPackageStartupMessages(library(S7))
# Create a generic
bizarro <- new_generic("bizarro", "x")
# Register some methods
method(bizarro, class_numeric) <- function(x) rev(x)
method(bizarro, new_S3_class("data.frame")) <- function(x) {
  x[] <- lapply(x, bizarro)
  rev(x)
}

# Using a generic calls the methods automatically
bizarro(head(mtcars))