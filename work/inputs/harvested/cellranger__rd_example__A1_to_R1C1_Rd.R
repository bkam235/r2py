# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: A1_to_R1C1.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 6

suppressPackageStartupMessages(library(cellranger))
A1_to_R1C1("$A$1")
A1_to_R1C1("A1")                 ## raises a warning, returns NA
A1_to_R1C1("A1", strict = FALSE) ## unless strict = FALSE
A1_to_R1C1(c("A1", "B$4")) ## raises a warning, includes an NA, because
A1_to_R1C1(c("A1", "B$4"), strict = FALSE) ## mixed ref always returns NA