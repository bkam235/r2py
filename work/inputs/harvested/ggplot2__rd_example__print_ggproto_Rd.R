# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: print.ggproto.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
Dog <- ggproto(
  print = function(self, n) {
    cat("Woof!\n")
  }
 )
Dog
cat(format(Dog), "\n")