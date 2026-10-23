# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: programming_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\programming.R
# lines: 8

suppressPackageStartupMessages(library(tidyr))
knitr::opts_chunk$set(collapse = TRUE, comment = "#>")
options(tibble.print_min = 6L, tibble.print_max = 6L)
set.seed(1014)

# Manually "import"; only needed for old dplyr which uses old tidyselect
# which doesn't attach automatically in tidy-select contexts
all_of <- tidyselect::all_of