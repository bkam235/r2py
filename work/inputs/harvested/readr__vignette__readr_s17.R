# r2py crawler metadata
# package: readr
# source_type: vignette
# topic: readr_s17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\doc\readr.R
# lines: 8

suppressPackageStartupMessages(library(readr))
df3 <- read_csv(
  readr_example("challenge.csv"), 
  col_types = list(
    x = col_double(),
    y = col_date(format = "")
  )
)