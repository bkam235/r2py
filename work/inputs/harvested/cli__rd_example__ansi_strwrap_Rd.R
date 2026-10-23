# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi_strwrap.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 9

suppressPackageStartupMessages(library(cli))
text <- cli:::lorem_ipsum()
# Highlight some words, that start with 's'
rexp <- gregexpr("\\b([sS][a-zA-Z]+)\\b", text)
regmatches(text, rexp) <- lapply(regmatches(text, rexp), col_red)
cat(text)

wrp <- ansi_strwrap(text, width = 40)
cat(wrp, sep = "\n")