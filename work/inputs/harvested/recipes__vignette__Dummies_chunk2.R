# r2py crawler metadata
# package: recipes
# source_type: vignette
# topic: Dummies_chunk2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\doc\Dummies.Rmd
# lines: 8

#| label: iris-base-rec
library(recipes)

# make a copy for use below
iris <- iris |> mutate(original = Species)

iris_rec <- recipe( ~ ., data = iris)
summary(iris_rec)