# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: googlesheets4-configuration.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 27

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
# message: "Creating new Sheet ..."
(ss <- gs4_create("gs4-quiet-demo", sheets = "alpha"))

# message: "Editing ..., Writing ..."
range_write(ss, data = data.frame(x = 1, y = "a"))

# suppress messages for a small amount of code
with_gs4_quiet(
  ss %>% sheet_append(data.frame(x = 2, y = "b"))
)

# message: "Writing ..., Appending ..."
ss %>% sheet_append(data.frame(x = 3, y = "c"))

# suppress messages until end of current scope
local_gs4_quiet()
ss %>% sheet_append(data.frame(x = 4, y = "d"))

# see that all the data was, in fact, written
read_sheet(ss)

# clean up
gs4_find("gs4-quiet-demo") %>%
  googledrive::drive_trash()
}) # examplesIf