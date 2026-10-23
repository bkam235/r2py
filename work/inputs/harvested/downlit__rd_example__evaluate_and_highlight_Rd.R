# r2py crawler metadata
# package: downlit
# source_type: rd_example
# topic: evaluate_and_highlight.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\downlit\help
# lines: 18

suppressPackageStartupMessages(library(downlit))
cat(evaluate_and_highlight("1 + 2"))
cat(evaluate_and_highlight("x <- 1:10\nmean(x)"))

# -----------------------------------------------------------------
# evaluate_and_highlight() powers pkgdown's documentation formatting so
# here I include a few examples to make sure everything looks good
# -----------------------------------------------------------------

blue <- function(x) paste0("\033[34m", x, "\033[39m")
f <- function(x) {
  cat("This is some output. My favourite colour is ", blue("blue"), ".\n", sep = "")
  message("This is a message. My favourite fruit is ", blue("blueberries"))
  warning("Now at stage ", blue("blue"), "!")
}
f()

plot(1:10)