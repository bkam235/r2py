# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: replace_na.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 14

suppressPackageStartupMessages(library(tidyr))
# Replace NAs in a data frame
df <- tibble(x = c(1, 2, NA), y = c("a", NA, "b"))
df |> replace_na(list(x = 0, y = "unknown"))

# Replace NAs in a vector
df |> dplyr::mutate(x = replace_na(x, 0))
# OR
df$x |> replace_na(0)
df$y |> replace_na("unknown")

# Replace NULLs in a list: NULLs are the list-col equivalent of NAs
df_list <- tibble(z = list(1:5, NULL, 10:20))
df_list |> replace_na(list(z = list(5)))