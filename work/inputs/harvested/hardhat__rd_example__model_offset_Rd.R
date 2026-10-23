# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: model_offset.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 19

suppressPackageStartupMessages(library(hardhat))
x <- model.frame(Species ~ offset(Sepal.Width), iris)

model_offset(terms(x), x)

xx <- model.frame(Species ~ offset(Sepal.Width) + offset(Sepal.Length), iris)

model_offset(terms(xx), xx)

# Problematic columns are caught with intuitive errors
tryCatch(
  expr = {
    x <- model.frame(~ offset(Species), iris)
    model_offset(terms(x), x)
  },
  error = function(e) {
    print(e$message)
  }
)