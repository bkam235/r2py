# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: googledrive-configuration.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 29

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# message: "Created Drive file"
(x <- drive_create("drive-quiet-demo", type = "document"))

# message: "File updated"
x <- drive_update(x, starred = TRUE)
drive_reveal(x, "starred")

# suppress messages for a small amount of code
with_drive_quiet(
  x <- drive_update(x, name = "drive-quiet-works")
)
x$name

# message: "File updated"
x <- drive_update(x, media = drive_example_local("chicken.txt"))

# suppress messages within a specific scope, e.g. function
unstar <- function(y) {
  local_drive_quiet()
  drive_update(y, starred = FALSE)
}
x <- unstar(x)
drive_reveal(x, "starred")

# Clean up
drive_rm(x)
}) # examplesIf