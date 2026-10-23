# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: format_delim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 13

suppressPackageStartupMessages(library(readr))
# format_()* functions are useful for testing and reprexes
cat(format_csv(mtcars))
cat(format_tsv(mtcars))
cat(format_delim(mtcars, ";"))

# Specifying missing values
df <- data.frame(x = c(1, NA, 3))
format_csv(df, na = "missing")

# Quotes are automatically added as needed
df <- data.frame(x = c("a ", '"', ",", "\n"))
cat(format_csv(df))