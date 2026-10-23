# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_update.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 26

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Create a new file, so we can update it
x <- drive_example_remote("chicken.csv") |>
  drive_cp()

# Update the file with new media
x <- x |>
  drive_update(drive_example_local("chicken.txt"))

# Update the file with new metadata.
# Notice here `name` is not an argument of `drive_update()`, we are passing
# this to the API via the `...``
x <- x |>
  drive_update(name = "CHICKENS!")

# Update the file with new media AND new metadata
x <- x |>
  drive_update(
    drive_example_local("chicken.txt"),
    name = "chicken-poem-again.txt"
  )

# Clean up
drive_rm(x)
}) # examplesIf