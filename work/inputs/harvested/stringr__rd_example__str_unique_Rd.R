# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: str_unique.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 9

suppressPackageStartupMessages(library(stringr))
str_unique(c("a", "b", "c", "b", "a"))

str_unique(c("a", "b", "c", "B", "A"))
str_unique(c("a", "b", "c", "B", "A"), ignore_case = TRUE)

# Use ... to pass additional arguments to stri_unique()
str_unique(c("motley", "mÃ¶tley", "pinguino", "pingÃ¼ino"))
str_unique(c("motley", "mÃ¶tley", "pinguino", "pingÃ¼ino"), strength = 1)