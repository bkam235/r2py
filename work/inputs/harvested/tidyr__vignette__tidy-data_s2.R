# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: tidy-data_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\tidy-data.R
# lines: 10

suppressPackageStartupMessages(library(tidyr))
library(tibble)
classroom <- tribble(
  ~name,    ~quiz1, ~quiz2, ~test1,
  "Billy",  NA,     "D",    "C",
  "Suzy",   "F",    NA,     NA,
  "Lionel", "B",    "C",    "B",
  "Jenny",  "A",    "A",    "B"
  )
classroom