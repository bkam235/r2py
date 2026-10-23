# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s58
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 11

suppressPackageStartupMessages(library(tidyr))
spec <- tribble(
  ~.name,            ~.value, ~units,  ~region,
  "1 unit",          "n",     "1",     NA,
  "2 to 4 units",    "n",     "2-4",   NA,
  "5 units or more", "n",     "5+",    NA,
  "Northeast",       "n",     NA,      "Northeast",
  "Midwest",         "n",     NA,      "Midwest",
  "South",           "n",     NA,      "South",
  "West",            "n",     NA,      "West",
)