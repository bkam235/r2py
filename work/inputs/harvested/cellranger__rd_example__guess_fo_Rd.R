# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: guess_fo.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 9

suppressPackageStartupMessages(library(cellranger))
A1 <- c("A1", "$A1", "A$1", "$A$1", "a1")
guess_fo(A1)
R1C1 <- c("R1C1", "R1C[-1]", "R[-1]C1", "R[-1]C[9]")
guess_fo(R1C1)

guess_fo("RC2")
guess_fo("12")
guess_fo(12)