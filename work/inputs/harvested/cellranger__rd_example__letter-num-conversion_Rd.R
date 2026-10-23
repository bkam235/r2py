# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: letter-num-conversion.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 9

suppressPackageStartupMessages(library(cellranger))
letter_to_num('Z')
letter_to_num(c('AA', 'ZZ', 'ABD', 'ZZZ'))
letter_to_num(c(NA, ''))
num_to_letter(28)
num_to_letter(900)
num_to_letter(18278)
num_to_letter(c(25, 52, 900, 18278))
num_to_letter(c(NA, 0, 4.8, -4))