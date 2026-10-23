# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_chunk7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.Rmd
# lines: 4

suppressPackageStartupMessages(library(dplyr))
for (var in names(mtcars)) {
      mtcars |> count(.data[[var]]) |> print()
    }