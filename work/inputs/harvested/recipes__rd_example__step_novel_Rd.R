# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_novel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 25

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("modeldata")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(Sacramento, package = "modeldata")

sacr_tr <- Sacramento[1:800, ]
sacr_te <- Sacramento[801:806, ]

# Without converting the predictor to a character, the new level would be converted
# to `NA`.
sacr_te$city <- as.character(sacr_te$city)
sacr_te$city[3] <- "beeptown"
sacr_te$city[4] <- "boopville"
sacr_te$city <- as.factor(sacr_te$city)

rec <- recipe(~ city + zip, data = sacr_tr)

rec <- rec |>
  step_novel(city, zip)
rec <- prep(rec, training = sacr_tr)

processed <- bake(rec, sacr_te)
tibble(old = sacr_te$city, new = processed$city)

tidy(rec, number = 1)
}) # examplesIf