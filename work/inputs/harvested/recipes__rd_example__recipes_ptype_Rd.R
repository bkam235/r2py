# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: recipes_ptype.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 31

suppressPackageStartupMessages(library(recipes))
training <- tibble(
  y = 1:10,
  id = 1:10,
  x1 = letters[1:10],
  x2 = factor(letters[1:10]),
  cw = hardhat::importance_weights(1:10)
)
training

rec_spec <- recipe(y ~ ., data = training)

# outcomes and case_weights are not required at bake time
recipes_ptype(rec_spec, stage = "prep")
recipes_ptype(rec_spec, stage = "bake")

rec_spec <- recipe(y ~ ., data = training) |>
  update_role(x1, new_role = "id")

# outcomes and case_weights are not required at bake time
# "id" column is assumed to be needed
recipes_ptype(rec_spec, stage = "prep")
recipes_ptype(rec_spec, stage = "bake")

rec_spec <- recipe(y ~ ., data = training) |>
  update_role(x1, new_role = "id") |>
  update_role_requirements("id", bake = FALSE)

# update_role_requirements() is used to specify that "id" isn't needed
recipes_ptype(rec_spec, stage = "prep")
recipes_ptype(rec_spec, stage = "bake")