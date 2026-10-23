# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: rowwise_chunk32
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\rowwise.Rmd
# lines: 12

suppressPackageStartupMessages(library(dplyr))
df <- rowwise(tribble(
   ~rng,     ~params,
   "runif",  list(min = -1, max = 1),
   "rnorm",  list(),
   "rpois",  list(lambda = 5),
))

# Has to happen in separate function to avoid eager unquoting
f <- function(rng, params) purrr::exec(rng, n = 10, !!!params)
df |>
  mutate(data = list(f(rng, params)))