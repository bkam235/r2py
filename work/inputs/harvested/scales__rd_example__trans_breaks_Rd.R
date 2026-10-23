# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: trans_breaks.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 5

suppressPackageStartupMessages(library(scales))
trans_breaks("log10", function(x) 10^x)(c(1, 1e6))
trans_breaks("sqrt", function(x) x^2)(c(1, 100))
trans_breaks(function(x) 1 / x, function(x) 1 / x)(c(1, 100))
trans_breaks(function(x) -x, function(x) -x)(c(1, 100))