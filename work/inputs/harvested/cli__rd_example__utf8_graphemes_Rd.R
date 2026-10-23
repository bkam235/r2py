# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: utf8_graphemes.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 10

suppressPackageStartupMessages(library(cli))
# Five grapheme clusters
str <- paste0(
  "\U0001f477\U0001f3ff\u200d\u2640\ufe0f",
  "\U0001f477\U0001f3ff",
  "\U0001f477\u200d\u2640\ufe0f",
  "\U0001f477\U0001f3fb",
  "\U0001f477\U0001f3ff")
cat(str, "\n")
chrs <- utf8_graphemes(str)