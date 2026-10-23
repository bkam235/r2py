# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: local_bindings.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 7

suppressPackageStartupMessages(library(rlang))
foo <- "foo"
bar <- "bar"

# `foo` will be temporarily rebinded while executing `expr`
with_bindings(paste(foo, bar), foo = "rebinded")
paste(foo, bar)