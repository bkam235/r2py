# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: cell_addr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 6

suppressPackageStartupMessages(library(cellranger))
cell_addr(4, 3)
(ca <- cell_addr(1:4, 3))
ca[2:3]
ca[[4]]
length(ca)