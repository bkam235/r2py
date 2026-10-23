# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: mold.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 15

suppressPackageStartupMessages(library(hardhat))
if (rlang::is_installed(c("recipes"))) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
# See the method specific documentation linked in Description
# for the details of each blueprint, and more examples.

# XY
mold(iris["Sepal.Width"], iris$Species)

# Formula
mold(Species ~ Sepal.Width, iris)

# Recipe
library(recipes)
mold(recipe(Species ~ Sepal.Width, iris), iris)
}) # examplesIf