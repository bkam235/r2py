# r2py crawler metadata
# package: rmarkdown
# source_type: rd_example
# topic: pandoc_available.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rmarkdown\help
# lines: 7

library(rmarkdown)

if (pandoc_available())
  cat("pandoc", as.character(pandoc_version()), "is available!\n")

if (pandoc_available("1.12.3"))
  cat("required version of pandoc is available!\n")