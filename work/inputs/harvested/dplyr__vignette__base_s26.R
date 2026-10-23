# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: base_s26
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\base.R
# lines: 5

suppressPackageStartupMessages(library(dplyr))
iris |> select(1:3)
iris |> select(Species, Sepal.Length)
iris |> select(starts_with("Petal"))
iris |> select(where(is.factor))