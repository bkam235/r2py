# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: method.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 20

suppressPackageStartupMessages(library(S7))
# Create a generic and register some methods
bizarro <- new_generic("bizarro", "x")
method(bizarro, class_numeric) <- function(x) rev(x)
method(bizarro, class_factor) <- function(x) {
  levels(x) <- rev(levels(x))
  x
}

# Printing the generic shows the registered method
bizarro

# And you can use method() to inspect specific implementations
method(bizarro, class = class_integer)
method(bizarro, object = 1)
method(bizarro, class = class_factor)

# errors if method not found
try(method(bizarro, class = class_data.frame))
try(method(bizarro, object = "x"))