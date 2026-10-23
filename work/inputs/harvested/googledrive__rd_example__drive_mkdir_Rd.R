# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_mkdir.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 34

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Create folder named 'ghi', then another below named it 'jkl' and star it
ghi <- drive_mkdir("ghi")
jkl <- drive_mkdir("ghi/jkl", starred = TRUE)

# is 'jkl' really starred? YES
purrr::pluck(jkl, "drive_resource", 1, "starred")

# Another way to create folder 'mno' in folder 'ghi'
drive_mkdir("mno", path = "ghi")

# Yet another way to create a folder named 'pqr' in folder 'ghi',
# this time with parent folder stored in a dribble,
# and setting the new folder's description
pqr <- drive_mkdir("pqr", path = ghi, description = "I am a folder")

# Did we really set the description? YES
purrr::pluck(pqr, "drive_resource", 1, "description")

# `overwrite = FALSE` errors if something already exists at target filepath
# THIS WILL ERROR!
drive_create("name-squatter-mkdir", path = ghi)
drive_mkdir("name-squatter-mkdir", path = ghi, overwrite = FALSE)

# `overwrite = TRUE` moves the existing item to trash, then proceeds
drive_mkdir("name-squatter-mkdir", path = ghi, overwrite = TRUE)

# list everything inside 'ghi'
drive_ls("ghi")

# Clean up
drive_rm(ghi)
}) # examplesIf