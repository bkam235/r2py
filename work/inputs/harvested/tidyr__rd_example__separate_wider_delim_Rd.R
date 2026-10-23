# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: separate_wider_delim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 48

suppressPackageStartupMessages(library(tidyr))
df <- tibble(id = 1:3, x = c("m-123", "f-455", "f-123"))
# There are three basic ways to split up a string into pieces:
# 1. with a delimiter
df |> separate_wider_delim(x, delim = "-", names = c("gender", "unit"))
# 2. by length
df |> separate_wider_position(x, c(gender = 1, 1, unit = 3))
# 3. defining each component with a regular expression
df |> separate_wider_regex(x, c(gender = ".", ".", unit = "\\d+"))

# Sometimes you split on the "last" delimiter
df <- tibble(var = c("race_1", "race_2", "age_bucket_1", "age_bucket_2"))
# _delim won't help because it always splits on the first delimiter
try(df |> separate_wider_delim(var, "_", names = c("var1", "var2")))
df |> separate_wider_delim(var, "_", names = c("var1", "var2"), too_many = "merge")
# Instead, you can use _regex
df |> separate_wider_regex(var, c(var1 = ".*", "_", var2 = ".*"))
# this works because * is greedy; you can mimic the _delim behaviour with .*?
df |> separate_wider_regex(var, c(var1 = ".*?", "_", var2 = ".*"))

# If the number of components varies, it's most natural to split into rows
df <- tibble(id = 1:4, x = c("x", "x y", "x y z", NA))
df |> separate_longer_delim(x, delim = " ")
# But separate_wider_delim() provides some tools to deal with the problem
# The default behaviour tells you that there's a problem
try(df |> separate_wider_delim(x, delim = " ", names = c("a", "b")))
# You can get additional insight by using the debug options
df |>
  separate_wider_delim(
    x,
    delim = " ",
    names = c("a", "b"),
    too_few = "debug",
    too_many = "debug"
  )

# But you can suppress the warnings
df |>
  separate_wider_delim(
    x,
    delim = " ",
    names = c("a", "b"),
    too_few = "align_start",
    too_many = "merge"
  )

# Or choose to automatically name the columns, producing as many as needed
df |> separate_wider_delim(x, delim = " ", names_sep = "", too_few = "align_start")