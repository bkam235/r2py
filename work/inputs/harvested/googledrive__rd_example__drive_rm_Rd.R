# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_rm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 20

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Target one of the official example files to copy (then remove)
(src_file <- drive_example_remote("chicken.txt"))

# Create a copy, then remove it by name
src_file |>
  drive_cp(name = "chicken-rm.txt")
drive_rm("chicken-rm.txt")

# Create several more copies
x1 <- src_file |>
  drive_cp(name = "chicken-abc.txt")
drive_cp(src_file, name = "chicken-def.txt")
x2 <- src_file |>
  drive_cp(name = "chicken-ghi.txt")

# Remove the copies all at once, specified in different ways
drive_rm(x1, "chicken-def.txt", as_id(x2))
}) # examplesIf