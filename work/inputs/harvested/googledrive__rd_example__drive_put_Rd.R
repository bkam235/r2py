# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_put.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 25

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# create a local file to work with
local_file <- tempfile("drive_put_", fileext = ".txt")
writeLines(c("beginning", "middle"), local_file)

# PUT to a novel filepath --> drive_put() delegates to drive_upload()
file <- drive_put(local_file)

# update the local file
cat("end", file = local_file, sep = "\n", append = TRUE)

# PUT again --> drive_put() delegates to drive_update()
file <- drive_put(local_file)

# create a second file at this filepath
file2 <- drive_create(basename(local_file))

# PUT again --> ERROR
drive_put(local_file)

# Clean up
drive_find("drive_put_.+[.]txt") |> drive_rm()
unlink(local_file)
}) # examplesIf