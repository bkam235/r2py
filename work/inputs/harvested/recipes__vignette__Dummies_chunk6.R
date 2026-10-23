# r2py crawler metadata
# package: recipes
# source_type: vignette
# topic: Dummies_chunk6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\doc\Dummies.Rmd
# lines: 7

suppressPackageStartupMessages(library(recipes))
#| label: mm-int
model.matrix(~ Species*Sepal.Length, data = iris) |> 
  as.data.frame() |> 
  # show a few specific rows
  slice(c(1, 51, 101)) |> 
  as.data.frame()