# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: sheet_write.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 36

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
df <- data.frame(
  x = 1:3,
  y = letters[1:3]
)

# specify only a data frame, get a new Sheet, with a random name
ss <- write_sheet(df)
read_sheet(ss)

# clean up
googledrive::drive_trash(ss)

# create a Sheet with some initial, placeholder data
ss <- gs4_create(
  "sheet-write-demo",
  sheets = list(alpha = data.frame(x = 1), omega = data.frame(x = 1))
)

# write df into its own, new sheet
sheet_write(df, ss = ss)

# write mtcars into the sheet named "omega"
sheet_write(mtcars, ss = ss, sheet = "omega")

# get an overview of the sheets
sheet_properties(ss)

# view your magnificent creation in the browser
gs4_browse(ss)

# clean up
gs4_find("sheet-write-demo") %>%
  googledrive::drive_trash()
}) # examplesIf