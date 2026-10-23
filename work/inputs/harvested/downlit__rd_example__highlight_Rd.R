# r2py crawler metadata
# package: downlit
# source_type: rd_example
# topic: highlight.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\downlit\help
# lines: 6

suppressPackageStartupMessages(library(downlit))
cat(highlight("1 + 1"))
cat(highlight("base::t(1:3)"))

# Unparseable R code returns NA
cat(highlight("base::t("))