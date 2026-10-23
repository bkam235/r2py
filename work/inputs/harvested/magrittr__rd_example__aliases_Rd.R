# r2py crawler metadata
# package: magrittr
# source_type: rd_example
# topic: aliases.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\help
# lines: 18

suppressPackageStartupMessages(library(magrittr))
iris %>%
   extract(, 1:4) %>%
   head

good.times <-
  Sys.Date() %>%
  as.POSIXct %>%
  seq(by = "15 mins", length.out = 100) %>%
  data.frame(timestamp = .)

good.times$quarter <-
  good.times %>%
  use_series(timestamp) %>%
  format("%M") %>%
  as.numeric %>%
  divide_by_int(15) %>%
  add(1)