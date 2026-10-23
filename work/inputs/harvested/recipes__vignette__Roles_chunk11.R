# r2py crawler metadata
# package: recipes
# source_type: vignette
# topic: Roles_chunk11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\doc\Roles.Rmd
# lines: 15

suppressPackageStartupMessages(library(recipes))
#| label = "dummy"
recipe( ~ ., data = iris) |> 
  step_dummy(Species) |> 
  prep() |> 
  bake(new_data = NULL, all_predictors()) |> 
  dplyr::select(starts_with("Species")) |> 
  names()

# or something else
recipe( ~ ., data = iris) |> 
  step_dummy(Species, role = "trousers") |> 
  prep() |> 
  bake(new_data = NULL, has_role("trousers")) |> 
  names()