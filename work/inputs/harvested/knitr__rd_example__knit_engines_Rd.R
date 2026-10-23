# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: knit_engines.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 4

suppressPackageStartupMessages(library(knitr))
knit_engines$get("python")
knit_engines$get("awk")
names(knit_engines$get())