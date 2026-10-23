# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: detect.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 26

suppressPackageStartupMessages(library(purrr))
is_even <- function(x) x %% 2 == 0

3:10 |> detect(is_even)
3:10 |> detect_index(is_even)

3:10 |> detect(is_even, .dir = "backward")
3:10 |> detect_index(is_even, .dir = "backward")


# Since `.f` is passed to as_mapper(), you can supply a pluck object:
x <- list(
  list(1, foo = FALSE),
  list(2, foo = TRUE),
  list(3, foo = TRUE)
)

detect(x, "foo")
detect_index(x, "foo")


# If you need to find all values, use keep():
keep(x, "foo")

# If you need to find all positions, use map_lgl():
which(map_lgl(x, "foo"))