# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: separate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 33

suppressPackageStartupMessages(library(tidyr))
# If you want to split by any non-alphanumeric value (the default):
df <- tibble(x = c(NA, "x.y", "x.z", "y.z"))
df |> separate(x, c("A", "B"))

# If you just want the second variable:
df |> separate(x, c(NA, "B"))

# We now recommend separate_wider_delim() instead:
df |> separate_wider_delim(x, ".", names = c("A", "B"))
df |> separate_wider_delim(x, ".", names = c(NA, "B"))

# Controlling uneven splits -------------------------------------------------
# If every row doesn't split into the same number of pieces, use
# the extra and fill arguments to control what happens:
df <- tibble(x = c("x", "x y", "x y z", NA))
df |> separate(x, c("a", "b"))
# The same behaviour as previous, but drops the c without warnings:
df |> separate(x, c("a", "b"), extra = "drop", fill = "right")
# Opposite of previous, keeping the c and filling left:
df |> separate(x, c("a", "b"), extra = "merge", fill = "left")
# Or you can keep all three:
df |> separate(x, c("a", "b", "c"))

# To only split a specified number of times use extra = "merge":
df <- tibble(x = c("x: 123", "y: error: 7"))
df |> separate(x, c("key", "value"), ": ", extra = "merge")

# Controlling column types --------------------------------------------------
# convert = TRUE detects column classes:
df <- tibble(x = c("x:1", "x:2", "y:4", "z", NA))
df |> separate(x, c("key", "value"), ":") |> str()
df |> separate(x, c("key", "value"), ":", convert = TRUE) |> str()