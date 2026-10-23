# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_count.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 17

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(covers, package = "modeldata")

rec <- recipe(~description, covers) |>
  step_count(description, pattern = "(rock|stony)", result = "rocks") |>
  step_count(description, pattern = "famil", normalize = TRUE)

rec2 <- prep(rec, training = covers)
rec2

count_values <- bake(rec2, new_data = covers)
count_values

tidy(rec, number = 1)
tidy(rec2, number = 1)
}) # examplesIf