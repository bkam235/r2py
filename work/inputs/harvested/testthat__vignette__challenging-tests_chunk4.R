# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: challenging-tests_chunk4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\challenging-tests.Rmd
# lines: 16

suppressPackageStartupMessages(library(testthat))
#| label: continue

continue <- function(prompt) {
  cat(prompt, "\n", sep = "")

  repeat {
    val <- readline("Do you want to continue? (y/n) ")
    if (val %in% c("y", "n")) {
      return(val == "y")
    }
    cat("! You must enter y or n\n")
  }  
}

readline <- NULL