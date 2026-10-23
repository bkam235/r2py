# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: format_error_call.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 11

suppressPackageStartupMessages(library(rlang))
# Arguments are stripped
writeLines(format_error_call(quote(foo(bar, baz))))

# Returns `NULL` with complex calls such as those that contain
# inlined functions
format_error_call(call2(list))

# Operators are formatted using their names rather than in
# function call form
writeLines(format_error_call(quote(1 + 2)))