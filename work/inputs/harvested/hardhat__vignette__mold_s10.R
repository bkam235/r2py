# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: mold_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\mold.R
# lines: 6

suppressPackageStartupMessages(library(hardhat))
try({
mold(~ body_mass_g - 1, penguins)

mold(~ body_mass_g + 0, penguins)
})