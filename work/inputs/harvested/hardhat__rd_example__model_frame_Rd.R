# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: model_frame.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 21

suppressPackageStartupMessages(library(hardhat))
# ---------------------------------------------------------------------------
# Example usage

framed <- model_frame(Species ~ Sepal.Width, iris)

framed$data

framed$terms

# ---------------------------------------------------------------------------
# Missing values never result in dropped rows

iris2 <- iris
iris2$Sepal.Width[1] <- NA

framed2 <- model_frame(Species ~ Sepal.Width, iris2)

head(framed2$data)

nrow(framed2$data) == nrow(iris2)