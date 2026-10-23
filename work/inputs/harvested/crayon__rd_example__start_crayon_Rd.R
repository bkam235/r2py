# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: start.crayon.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\crayon\help
# lines: 10

suppressPackageStartupMessages(library(crayon))
## The input is red (if color is supported)
get_name <- function() {
  cat("Enter your name:", start(red))
  input <- readline()
  cat(finish(red))
  input
}
name <- get_name()
name