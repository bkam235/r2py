# r2py crawler metadata
# package: globals
# source_type: rd_example
# topic: globalsOf.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\globals\help
# lines: 11

suppressPackageStartupMessages(library(globals))
b <- 2
expr <- substitute({ a <- b; b <- 1 })

## Will _not_ identify 'b' (because it's also a local)
globalsC <- globalsOf(expr, method = "conservative")
print(globalsC)

## Will identify 'b'
globalsL <- globalsOf(expr, method = "liberal")
print(globalsL)