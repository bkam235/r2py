# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_language.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 4

suppressPackageStartupMessages(library(withr))
with_language("en", try(mean[[1]]))
with_language("fr", try(mean[[1]]))
with_language("es", try(mean[[1]]))