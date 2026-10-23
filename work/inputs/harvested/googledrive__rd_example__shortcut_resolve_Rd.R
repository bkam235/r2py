# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: shortcut_resolve.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 33

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Create a file to make a shortcut to
file <- drive_example_remote("chicken_sheet") |>
  drive_cp(name = "chicken-sheet-for-shortcut")

# Create a shortcut
sc1 <- file |>
  shortcut_create(name = "shortcut-1")

# Create a second shortcut by copying the first
sc1 <- sc1 |>
  drive_cp(name = "shortcut-2")

# Get the shortcuts
(sc_dat <- drive_find("-[12]$", type = "shortcut"))

# Resolve them
(resolved <- shortcut_resolve(sc_dat))

resolved$id
file$id

# Delete the target file
drive_rm(file)

# (Try to) resolve the shortcuts again
shortcut_resolve(sc_dat)
# No error, but resolution is unsuccessful due to non-existent target

# Clean up
drive_rm(sc_dat)
}) # examplesIf