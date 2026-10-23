# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_publish.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 17

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Create a file to publish
file <- drive_example_remote("chicken_sheet") |>
  drive_cp()

# Publish file
file <- drive_publish(file)
file$published

# Unpublish file
file <- drive_unpublish(file)
file$published

# Clean up
drive_rm(file)
}) # examplesIf