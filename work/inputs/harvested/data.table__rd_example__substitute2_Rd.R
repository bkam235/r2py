# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: substitute2.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 41

suppressPackageStartupMessages(library(data.table))
## base R substitute vs substitute2
substitute(list(var1 = var2), list(var1 = "c1", var2 = 5L))
substitute2(list(var1 = var2), list(var1 = "c1", var2 = 5L)) ## works also on names

substitute(var1, list(var1 = "c1"))
substitute2(var1, list(var1 = I("c1"))) ## enforce character with I

substitute(var1, list(var1 = as.name("c1")))
substitute2(var1, list(var1 = "c1")) ## turn character into symbol, for convenience

## mix symbols and characters using 'I' function, both lines will yield same result
substitute2(list(var1 = var2), list(var1 = "c1", var2 = I("some_character")))
substitute2(list(var1 = var2), I(list(var1 = as.name("c1"), var2 = "some_character")))

## list elements are enlist'ed into list calls
(cl1 = substitute(f(lst), list(lst = list(1L, 2L))))
(cl2 = substitute2(f(lst), I(list(lst = list(1L, 2L)))))
(cl3 = substitute2(f(lst), list(lst = I(list(1L, 2L)))))
(cl4 = substitute2(f(lst), list(lst = quote(list(1L, 2L)))))
(cl5 = substitute2(f(lst), list(lst = list(1L, 2L))))
cl1[[2L]] ## base R substitute with list element
cl2[[2L]] ## same
cl3[[2L]] ## same
cl4[[2L]] ## desired
cl5[[2L]] ## automatically

## character to name and list into list calls works recursively
(cl1 = substitute2(f(lst), list(lst = list(1L, list(2L)))))
(cl2 = substitute2(f(lst), I(list(lst = list(1L, list(2L)))))) ## unless I() used
last(cl1[[2L]]) ## enlisted recursively
last(cl2[[2L]]) ## AsIs

## using substitute2 from another function
f = function(expr, env) {
  eval(substitute(
    substitute2(.expr, env),
    list(.expr = substitute(expr))
  ))
}
f(list(var1 = var2), list(var1 = "c1", var2 = 5L))