# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: top_n.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 13

suppressPackageStartupMessages(library(dplyr))
df <- data.frame(x = c(6, 4, 1, 10, 3, 1, 1))

df |> top_n(2)  # highest values
df |> top_n(-2) # lowest values
# now use
df |> slice_max(x, n = 2)
df |> slice_min(x, n = 2)

# top_frac() -> prop argument of slice_min()/slice_max()
df |> top_frac(.5)
# ->
df |> slice_max(x, prop = 0.5)