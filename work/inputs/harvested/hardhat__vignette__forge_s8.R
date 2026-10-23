# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: forge_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\forge.R
# lines: 7

suppressPackageStartupMessages(library(hardhat))
try({
test_species_double <- penguin_test
test_species_double$species <- as.double(test_species_double$species)

forge(test_species_double, formula_eng)
})