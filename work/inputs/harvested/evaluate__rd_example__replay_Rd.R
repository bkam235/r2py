# r2py crawler metadata
# package: evaluate
# source_type: rd_example
# topic: replay.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\evaluate\help
# lines: 17

suppressPackageStartupMessages(library(evaluate))
f1 <- function() {
  cat("1\n")
  print("2")
  warning("3")
  print("4")
  message("5")
  stop("6")
}
replay(evaluate("f1()"))

f2 <- function() {
  message("Hello")
  plot(1:10)
  message("Goodbye")
}
replay(evaluate("f2()"))