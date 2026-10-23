# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: step_harmonic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 72

suppressPackageStartupMessages(library(recipes))
if (rlang::is_installed("ggplot2")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
library(ggplot2, quietly = TRUE)
library(dplyr)

data(sunspot.year)
sunspots <-
  tibble(
    year = 1700:1988,
    n_sunspot = sunspot.year,
    type = "measured"
  ) |>
  slice(1:75)

# sunspots period is around 11 years, sample spacing is one year
dat <- recipe(n_sunspot ~ year, data = sunspots) |>
  step_harmonic(year, frequency = 1 / 11, cycle_size = 1) |>
  prep() |>
  bake(new_data = NULL)

fit <- lm(n_sunspot ~ year_sin_1 + year_cos_1, data = dat)

preds <- tibble(
  year = sunspots$year,
  n_sunspot = fit$fitted.values,
  type = "predicted"
)

bind_rows(sunspots, preds) |>
  ggplot(aes(x = year, y = n_sunspot, color = type)) +
  geom_line()


# POSIXct example

date_time <-
  as.POSIXct(
    paste0(rep(1959:1997, each = 12), "-", rep(1:12, length(1959:1997)), "-01"),
    tz = "UTC"
  )

carbon_dioxide <- tibble(
  date_time = date_time,
  co2 = as.numeric(co2),
  type = "measured"
)

# yearly co2 fluctuations
dat <-
  recipe(co2 ~ date_time,
    data = carbon_dioxide
  ) |>
  step_mutate(date_time_num = as.numeric(date_time)) |>
  step_ns(date_time_num, deg_free = 3) |>
  step_harmonic(date_time, frequency = 1, cycle_size = 86400 * 365.24) |>
  prep() |>
  bake(new_data = NULL)

fit <- lm(co2 ~ date_time_num_ns_1 + date_time_num_ns_2 +
  date_time_num_ns_3 + date_time_sin_1 +
  date_time_cos_1, data = dat)

preds <- tibble(
  date_time = date_time,
  co2 = fit$fitted.values,
  type = "predicted"
)

bind_rows(carbon_dioxide, preds) |>
  ggplot(aes(x = date_time, y = co2, color = type)) +
  geom_line()
}) # examplesIf