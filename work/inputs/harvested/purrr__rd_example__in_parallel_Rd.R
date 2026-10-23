# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: in_parallel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 29

suppressPackageStartupMessages(library(purrr))
if (interactive() && rlang::is_installed("mirai") && rlang::is_installed("carrier")) withAutoprint({ # examplesIf
# Run in interactive sessions only as spawns additional processes

default_param <- 0.5

delay <- function(secs = default_param) {
  Sys.sleep(secs)
}

slow_lm <- function(formula, data) {
  delay()
  lm(formula, data)
}

# Example of a 'crate' returned by in_parallel(). The object print method
# shows the size of the crate and any objects contained within:
crate <- in_parallel(
  \(df) slow_lm(mpg ~ disp, data = df),
  slow_lm = slow_lm,
  delay = delay,
  default_param = default_param
)
crate

# Use mirai::mirai() to test that a crate is self-contained
# by running it in a daemon and collecting its return value:
mirai::mirai(crate(mtcars), crate = crate) |> mirai::collect_mirai()
}) # examplesIf