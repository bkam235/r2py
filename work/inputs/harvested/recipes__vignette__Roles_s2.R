# r2py crawler metadata
# package: recipes
# source_type: vignette
# topic: Roles_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\doc\Roles.R
# lines: 7

library(recipes)

recipe(Species ~ ., data = iris) |> summary()

recipe( ~ Species, data = iris) |> summary()

recipe(Sepal.Length + Sepal.Width ~ ., data = iris) |> summary()