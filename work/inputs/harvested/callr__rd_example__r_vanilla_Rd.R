# r2py crawler metadata
# package: callr
# source_type: rd_example
# topic: r_vanilla.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\callr\help
# lines: 9

suppressPackageStartupMessages(library(callr))
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
# Compare to r()
r(function() .libPaths())
r_vanilla(function() .libPaths())

r(function() getOption("repos"))
r_vanilla(function() getOption("repos"))
}) # examplesIf