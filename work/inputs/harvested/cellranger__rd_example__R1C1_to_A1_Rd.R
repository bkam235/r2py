# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: R1C1_to_A1.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 4

suppressPackageStartupMessages(library(cellranger))
R1C1_to_A1("R1C1")
R1C1_to_A1("R10C52", strict = FALSE)
R1C1_to_A1(c("R1C1", "R10C52", "RC4", "R[-3]C[9]"))