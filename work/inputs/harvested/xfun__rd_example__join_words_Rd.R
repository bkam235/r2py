# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: join_words.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 8

suppressPackageStartupMessages(library(xfun))
join_words("a")
join_words(c("a", "b"))
join_words(c("a", "b", "c"))
join_words(c("a", "b", "c"), sep = " / ", and = "")
join_words(c("a", "b", "c"), and = "")
join_words(c("a", "b", "c"), before = "\"", after = "\"")
join_words(c("a", "b", "c"), before = "\"", after = "\"", oxford_comma = FALSE)