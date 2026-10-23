# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: consecutive_id.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 7

suppressPackageStartupMessages(library(dplyr))
consecutive_id(c(TRUE, TRUE, FALSE, FALSE, TRUE, FALSE, NA, NA))
consecutive_id(c(1, 1, 1, 2, 1, 1, 2, 2))

df <- data.frame(x = c(0, 0, 1, 0), y = c(2, 2, 2, 2))
df |> group_by(x, y) |> summarise(n = n())
df |> group_by(id = consecutive_id(x, y), x, y) |> summarise(n = n())