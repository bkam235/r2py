# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_impute_linear.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 29

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed(c("modeldata", "ggplot2"))) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
data(ames, package = "modeldata")
set.seed(393)
ames_missing <- ames
ames_missing$Longitude[sample(1:nrow(ames), 200)] <- NA

imputed_ames <-
  recipe(Sale_Price ~ ., data = ames_missing) |>
  step_impute_linear(
    Longitude,
    impute_with = c(Latitude, Neighborhood, MS_Zoning, Alley)
  ) |>
  prep(ames_missing)

imputed <-
  bake(imputed_ames, new_data = ames_missing) |>
  dplyr::rename(imputed = Longitude) |>
  bind_cols(ames |> dplyr::select(original = Longitude)) |>
  bind_cols(ames_missing |> dplyr::select(Longitude)) |>
  dplyr::filter(is.na(Longitude))

library(ggplot2)
ggplot(imputed, aes(x = original, y = imputed)) +
  geom_abline(col = "green") +
  geom_point(alpha = .3) +
  coord_equal() +
  labs(title = "Imputed Values")
}) # examplesIf