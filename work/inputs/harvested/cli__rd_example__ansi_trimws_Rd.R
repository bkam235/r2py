# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi_trimws.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 5

suppressPackageStartupMessages(library(cli))
trimws(paste0("   ", col_red("I am red"), "   "))
ansi_trimws(paste0("   ", col_red("I am red"), "   "))
trimws(col_red("   I am red   "))
ansi_trimws(col_red("   I am red   "))