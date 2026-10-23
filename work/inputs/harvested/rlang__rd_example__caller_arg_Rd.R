# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: caller_arg.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 10

suppressPackageStartupMessages(library(rlang))
arg_checker <- function(x, arg = caller_arg(x), call = caller_env()) {
  cli::cli_abort("{.arg {arg}} must be a thingy.", arg = arg, call = call)
}

my_function <- function(my_arg) {
  arg_checker(my_arg)
}

try(my_function(NULL))