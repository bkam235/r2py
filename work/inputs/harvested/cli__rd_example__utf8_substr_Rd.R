# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: utf8_substr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 11

suppressPackageStartupMessages(library(cli))
# Five grapheme clusters, select the middle three
str <- paste0(
  "\U0001f477\U0001f3ff\u200d\u2640\ufe0f",
  "\U0001f477\U0001f3ff",
  "\U0001f477\u200d\u2640\ufe0f",
  "\U0001f477\U0001f3fb",
  "\U0001f477\U0001f3ff")
cat(str)
str24 <- utf8_substr(str, 2, 4)
cat(str24)