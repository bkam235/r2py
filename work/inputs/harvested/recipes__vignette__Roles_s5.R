# r2py crawler metadata
# package: recipes
# source_type: vignette
# topic: Roles_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\doc\Roles.R
# lines: 5

suppressPackageStartupMessages(library(recipes))
try({
recipe(HHV ~ ., data = biomass) |> 
  update_role(sample, new_role = NA_character_)
})