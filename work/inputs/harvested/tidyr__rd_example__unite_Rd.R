# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: unite.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 13

suppressPackageStartupMessages(library(tidyr))
df <- expand_grid(x = c("a", NA), y = c("b", NA))
df

df |> unite("z", x:y, remove = FALSE)
# To remove missing values:
df |> unite("z", x:y, na.rm = TRUE, remove = FALSE)

# Separate is almost the complement of unite
df |>
  unite("xy", x:y) |>
  separate(xy, c("x", "y"))
# (but note `x` and `y` contain now "NA" not NA)