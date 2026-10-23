# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: package_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\package.R
# lines: 6

suppressPackageStartupMessages(library(hardhat))
try({
multi_outcome <- mold(bill_length_mm + bill_depth_mm ~ body_mass_g + species, penguins)

simple_lm_bridge(multi_outcome)
})