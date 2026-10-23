# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: new_generic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 28

suppressPackageStartupMessages(library(S7))
# A simple generic with methods for some base types and S3 classes
type_of <- new_generic("type_of", dispatch_args = "x")
method(type_of, class_character) <- function(x, ...) "A character vector"
method(type_of, new_S3_class("data.frame")) <- function(x, ...) "A data frame"
method(type_of, class_function) <- function(x, ...) "A function"

type_of(mtcars)
type_of(letters)
type_of(mean)

# If you want to require that methods implement additional arguments,
# you can use a custom function:
mean2 <- new_generic("mean2", "x", function(x, ..., na.rm = FALSE) {
   S7_dispatch()
})

method(mean2, class_numeric) <- function(x, ..., na.rm = FALSE) {
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  sum(x) / length(x)
}

# You'll be warned if you forget the argument:
method(mean2, class_character) <- function(x, ...) {
  stop("Not supported")
}