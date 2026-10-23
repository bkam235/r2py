# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: range_autofit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 30

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
dat <- tibble::tibble(
  fruit = c("date", "lime", "pear", "plum")
)

ss <- gs4_create("range-autofit-demo", sheets = dat)
ss

# open in the browser
gs4_browse(ss)

# shrink column A to fit the short fruit names
range_autofit(ss)
# in the browser, notice how the column width shrank

# send some longer fruit names
dat2 <- tibble::tibble(
  fruit = c("cucumber", "honeydew")
)
ss %>% sheet_append(dat2)
# in the browser, see that column A is now too narrow to show the data

range_autofit(ss)
# in the browser, see the column A reveals all the data now

# clean up
gs4_find("range-autofit-demo") %>%
  googledrive::drive_trash()
}) # examplesIf