# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: tidy-data_chunk23
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\tidy-data.Rmd
# lines: 8

suppressPackageStartupMessages(library(tidyr))
library(purrr)
library(readr)

paths <- dir("data", pattern = "\\.csv$", full.names = TRUE)
names(paths) <- basename(paths)

map(paths, read_csv) |> list_rbind(names_to = "filename")