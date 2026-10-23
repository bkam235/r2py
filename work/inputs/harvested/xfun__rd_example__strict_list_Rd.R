# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: strict_list.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 12

library(xfun)
(z = strict_list(aaa = "I am aaa", b = 1:5))
z$a  # NULL!
z$aaa  # I am aaa
z$b
z$c = "create a new element"

z2 = unclass(z)  # a normal list
z2$a  # partial matching

z3 = as_strict_list(z2)  # a strict list again
z3$a  # NULL again!