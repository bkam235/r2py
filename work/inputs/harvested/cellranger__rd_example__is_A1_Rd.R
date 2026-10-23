# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: is_A1.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 7

suppressPackageStartupMessages(library(cellranger))
is_A1("A1")
is_R1C1("A1")
is_R1C1("R4C12")

x <- c("A1", "$A4", "$b$12", "RC1", "R[-4]C9", "R5C3")
data.frame(x, is_A1(x), is_R1C1(x))