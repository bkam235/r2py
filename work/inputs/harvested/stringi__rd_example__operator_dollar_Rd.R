# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: operator_dollar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 10

suppressPackageStartupMessages(library(stringi))
"value='%d'" %s$% 3
"value='%d'" %s$% 1:3
"%s='%d'" %s$% list("value", 3)
"%s='%d'" %s$% list("value", 1:3)
"%s='%d'" %s$% list(c("a", "b", "c"), 1)
"%s='%d'" %s$% list(c("a", "b", "c"), 1:3)

x <- c("abcd", "\u00DF\u00B5\U0001F970", "abcdef")
cat("[%6s]" %s$% x, sep="\n")  # width used, not the number of bytes