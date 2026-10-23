# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: local_error_call.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 16

suppressPackageStartupMessages(library(rlang))
# Set a context for error messages
function() {
  local_error_call(quote(foo()))
  local_error_call(sys.call())
}

# Disable the context
function() {
  local_error_call(NULL)
}

# Use the caller's context
function() {
  local_error_call(caller_env())
}