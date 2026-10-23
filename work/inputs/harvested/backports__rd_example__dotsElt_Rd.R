# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: dotsElt.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 7

suppressPackageStartupMessages(library(backports))
# get function from namespace instead of possibly getting
# implementation shipped with recent R versions:
bp_...elt = getFromNamespace("...elt", "backports")

foo = function(n, ...) bp_...elt(n)
foo(n = 2, "a", "b", "c")