# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: quietly.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 11

suppressPackageStartupMessages(library(purrr))
f <- function() {
  print("Hi!")
  message("Hello")
  warning("How are ya?")
  "Gidday"
}
f()

f_quiet <- quietly(f)
str(f_quiet())