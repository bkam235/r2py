# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: rowwise_s31
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\rowwise.R
# lines: 11

suppressPackageStartupMessages(library(dplyr))
df <- tribble(
   ~rng,     ~params,
   "runif",  list(n = 10),
   "rnorm",  list(n = 20),
   "rpois",  list(n = 10, lambda = 5),
) |>
  rowwise()

df |>
  mutate(data = list(do.call(rng, params)))