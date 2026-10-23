# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: separate_longer_delim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 13

suppressPackageStartupMessages(library(tidyr))
df <- tibble(id = 1:4, x = c("x", "x y", "x y z", NA))
df |> separate_longer_delim(x, delim = " ")

# You can separate multiple columns at once if they have the same structure
df <- tibble(id = 1:3, x = c("x", "x y", "x y z"), y = c("a", "a b", "a b c"))
df |> separate_longer_delim(c(x, y), delim = " ")

# Or instead split by a fixed length
df <- tibble(id = 1:3, x = c("ab", "def", ""))
df |> separate_longer_position(x, 1)
df |> separate_longer_position(x, 2)
df |> separate_longer_position(x, 2, keep_empty = TRUE)