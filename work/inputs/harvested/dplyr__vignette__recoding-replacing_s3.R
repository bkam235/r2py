# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: recoding-replacing_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\recoding-replacing.R
# lines: 7

suppressPackageStartupMessages(library(dplyr))
set.seed(123)
racers <- tibble(
  id = seq_len(100),
  time = round(sample(1200:2100, size = 100, replace = TRUE) / 60, 2)
)
racers