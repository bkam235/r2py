# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: cross.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 48

suppressPackageStartupMessages(library(purrr))
# We build all combinations of names, greetings and separators from our
# list of data and pass each one to paste()
data <- list(
  id = c("John", "Jane"),
  greeting = c("Hello.", "Bonjour."),
  sep = c("! ", "... ")
)

data |>
  cross() |>
  map(lift(paste))

# cross() returns the combinations in long format: many elements,
# each representing one combination. With cross_df() we'll get a
# data frame in long format: crossing three objects produces a data
# frame of three columns with each row being a particular
# combination. This is the same format that expand.grid() returns.
args <- data |> cross_df()

# In case you need a list in long format (and not a data frame)
# just run as.list() after cross_df()
args |> as.list()

# This format is often less practical for functional programming
# because applying a function to the combinations requires a loop
out <- vector("character", length = nrow(args))
for (i in seq_along(out))
  out[[i]] <- invoke("paste", map(args, i))
out

# It's easier to transpose and then use invoke_map()
args |> transpose() |> map_chr(\(x) exec(paste, !!!x))

# Unwanted combinations can be filtered out with a predicate function
filter <- function(x, y) x >= y
cross2(1:5, 1:5, .filter = filter) |> str()

# To give names to the components of the combinations, we map
# setNames() on the product:
x <- seq_len(3)
cross2(x, x, .filter = `==`) |>
  map(setNames, c("x", "y"))

# Alternatively we can encapsulate the arguments in a named list
# before crossing to get named components:
list(x = x, y = x) |>
  cross(.filter = `==`)