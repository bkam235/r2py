# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: diff_str.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 4

suppressPackageStartupMessages(library(cli))
str1 <- "abcdefghijklmnopqrstuvwxyz"
str2 <- "PREabcdefgMIDDLEnopqrstuvwxyzPOST"
diff_str(str1, str2)