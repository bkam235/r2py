# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: PercentAxis.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 4

suppressPackageStartupMessages(library(prodlim))
plot(0,0,xlim=c(0,1),ylim=c(0,1),axes=FALSE)
  PercentAxis(1,at=seq(0,1,.25))
  PercentAxis(2,at=seq(0,1,.25))