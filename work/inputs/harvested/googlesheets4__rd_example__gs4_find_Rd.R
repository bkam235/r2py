# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: gs4_find.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 14

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
# see all your Sheets
gs4_find()

# see 5 Sheets, prioritized by creation time
x <- gs4_find(order_by = "createdTime desc", n_max = 5)
x

# hoist the creation date, using other packages in the tidyverse
# x %>%
#   tidyr::hoist(drive_resource, created_on = "createdTime") %>%
#   dplyr::mutate(created_on = as.Date(created_on))
}) # examplesIf