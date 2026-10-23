# r2py crawler metadata
# package: rmarkdown
# source_type: rd_example
# topic: find_pandoc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rmarkdown\help
# lines: 4

suppressPackageStartupMessages(library(rmarkdown))
rmarkdown::find_pandoc()
rmarkdown::find_pandoc(dir = '~/Downloads/Pandoc')
rmarkdown::find_pandoc(version = '2.7.3')