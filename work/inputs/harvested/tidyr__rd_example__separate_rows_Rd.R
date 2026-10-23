# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: separate_rows.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 11

suppressPackageStartupMessages(library(tidyr))
df <- tibble(
  x = 1:3,
  y = c("a", "d,e,f", "g,h"),
  z = c("1", "2,3,4", "5,6")
)
separate_rows(df, y, z, convert = TRUE)

# Now recommended
df |>
  separate_longer_delim(c(y, z), delim = ",")