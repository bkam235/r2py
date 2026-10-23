# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: range_write.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 34

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
# create a Sheet with some initial, empty (work)sheets
(ss <- gs4_create("range-write-demo", sheets = c("alpha", "beta")))

df <- data.frame(
  x = 1:3,
  y = letters[1:3]
)

#  write df somewhere other than the "upper left corner"
range_write(ss, data = df, range = "D6")

# view your magnificent creation in the browser
gs4_browse(ss)

# send data of disparate types to a 1-row rectangle
dat <- tibble::tibble(
  string = "string",
  logical = TRUE,
  datetime = Sys.time()
)
range_write(ss, data = dat, sheet = "beta", col_names = FALSE)

# send data of disparate types to a 1-column rectangle
dat <- tibble::tibble(
  x = list(Sys.time(), FALSE, "string")
)
range_write(ss, data = dat, range = "beta!C5", col_names = FALSE)

# clean up
gs4_find("range-write-demo") %>%
  googledrive::drive_trash()
}) # examplesIf