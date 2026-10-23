# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: call2.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 15

suppressPackageStartupMessages(library(rlang))
# fn can either be a string, a symbol or a call
call2("f", a = 1)
call2(quote(f), a = 1)
call2(quote(f()), a = 1)

#' Can supply arguments individually or in a list
call2(quote(f), a = 1, b = 2)
call2(quote(f), !!!list(a = 1, b = 2))

# Creating namespaced calls is easy:
call2("fun", arg = quote(baz), .ns = "mypkg")

# Empty arguments are preserved:
call2("[", quote(x), , drop = )