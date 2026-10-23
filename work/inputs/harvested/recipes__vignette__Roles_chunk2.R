# r2py crawler metadata
# package: recipes
# source_type: vignette
# topic: Roles_chunk2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\doc\Roles.Rmd
# lines: 8

#| label = "formula-roles"
library(recipes)

recipe(Species ~ ., data = iris) |> summary()

recipe( ~ Species, data = iris) |> summary()

recipe(Sepal.Length + Sepal.Width ~ ., data = iris) |> summary()