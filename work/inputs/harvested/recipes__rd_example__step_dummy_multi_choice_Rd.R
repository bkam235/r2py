# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_dummy_multi_choice.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 26

suppressPackageStartupMessages(library(recipes))
library(tibble)
languages <- tribble(
  ~lang_1,    ~lang_2,   ~lang_3,
  "English",  "Italian", NA,
  "Spanish",  NA,        "French",
  "Armenian", "English", "French",
  NA,         NA,        NA
)

dummy_multi_choice_rec <- recipe(~., data = languages) |>
  step_dummy_multi_choice(starts_with("lang")) |>
  prep()

bake(dummy_multi_choice_rec, new_data = NULL)
tidy(dummy_multi_choice_rec, number = 1)

dummy_multi_choice_rec2 <- recipe(~., data = languages) |>
  step_dummy_multi_choice(starts_with("lang"),
    prefix = "lang",
    threshold = 0.2
  ) |>
  prep()

bake(dummy_multi_choice_rec2, new_data = NULL)
tidy(dummy_multi_choice_rec2, number = 1)