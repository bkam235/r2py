# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: nest_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\nest.R
# lines: 9

suppressPackageStartupMessages(library(tidyr))
df2 <- tribble(
  ~g, ~x, ~y,
   1,  1,  2,
   2,  4,  6,
   2,  5,  7,
   3, 10,  NA
)
df2 |> nest(data = c(x, y))