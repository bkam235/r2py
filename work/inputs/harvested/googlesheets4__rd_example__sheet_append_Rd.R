# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: sheet_append.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 28

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
# we will recreate the table of "other" deaths from this example Sheet
(deaths <- gs4_example("deaths") %>%
  range_read(range = "other_data", col_types = "????DD"))

# split the data into 3 pieces, which we will send separately
deaths_one <- deaths[1:5, ]
deaths_two <- deaths[6, ]
deaths_three <- deaths[7:10, ]

# create a Sheet and send the first chunk of data
ss <- gs4_create("sheet-append-demo", sheets = list(deaths = deaths_one))

# append a single row
ss %>% sheet_append(deaths_two)

# append remaining rows
ss %>% sheet_append(deaths_three)

# read and check against the original
deaths_replica <- range_read(ss, col_types = "????DD")
identical(deaths, deaths_replica)

# clean up
gs4_find("sheet-append-demo") %>%
  googledrive::drive_trash()
}) # examplesIf