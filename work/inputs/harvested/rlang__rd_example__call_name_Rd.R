# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: call_name.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 26

suppressPackageStartupMessages(library(rlang))
# Is the function named?
is_call_simple(quote(foo()))
is_call_simple(quote(foo[[1]]()))

# Is the function namespaced?
is_call_simple(quote(list()), ns = TRUE)
is_call_simple(quote(base::list()), ns = TRUE)

# Extract the function name from quoted calls:
call_name(quote(foo(bar)))
call_name(quo(foo(bar)))

# Namespaced calls are correctly handled:
call_name(quote(base::matrix(baz)))

# Anonymous and subsetted functions return NULL:
call_name(quote(foo$bar()))
call_name(quote(foo[[bar]]()))
call_name(quote(foo()()))

# Extract namespace of a call with call_ns():
call_ns(quote(base::bar()))

# If not namespaced, call_ns() returns NULL:
call_ns(quote(bar()))