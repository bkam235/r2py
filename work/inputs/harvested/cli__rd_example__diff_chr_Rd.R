# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: diff_chr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 4

suppressPackageStartupMessages(library(cli))
letters2 <- c("P", "R", "E", letters, "P", "O", "S", "T")
letters2[11:16] <- c("M", "I", "D", "D", "L", "E")
diff_chr(letters, letters2)