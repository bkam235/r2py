# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: call_inspect.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 7

suppressPackageStartupMessages(library(rlang))
# When you call it directly, it simply returns what you typed
call_inspect(foo(bar), "" %>% identity())

# Pass `call_inspect` to functionals like `lapply()` or `map()` to
# inspect the calls they create around the supplied function
lapply(1:3, call_inspect)