# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: with_verbosity.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 10

suppressPackageStartupMessages(library(httr2))
fun <- function() {
  request("https://httr2.r-lib.org") |> req_perform()
}
with_verbosity(fun())

fun <- function() {
  local_verbosity(2)
  # someotherpackage::fun()
}