# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: map_if.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 12

suppressPackageStartupMessages(library(purrr))
# Use a predicate function to decide whether to map a function:
iris |> map_if(is.factor, as.character) |> str()

# Specify an alternative with the `.else` argument:
iris |> map_if(is.factor, as.character, .else = as.integer) |> str()

# Use numeric vector of positions select elements to change:
iris |> map_at(c(4, 5), is.numeric) |> str()

# Use vector of names to specify which elements to change:
iris |> map_at("Species", toupper) |> str()