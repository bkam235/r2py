# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: opts_knit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 8

suppressPackageStartupMessages(library(knitr))
opts_knit$get("verbose")
opts_knit$set(verbose = TRUE)  # change it
if (interactive()) {
    # for unnamed chunks, use 'fig' as the figure prefix
    opts_knit$set(unnamed.chunk.label = "fig")
    knit("001-minimal.Rmd")  # from https://github.com/yihui/knitr-examples
}