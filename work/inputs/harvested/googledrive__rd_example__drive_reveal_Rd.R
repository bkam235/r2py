# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_reveal.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 31

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# Get a few of your files
files <- drive_find(n_max = 10, trashed = NA)

# the "special" cases that require additional API calls and can be slow
drive_reveal(files, "path")
drive_reveal(files, "permissions")
drive_reveal(files, "published")

# a "special" case of digging info out of `drive_resource`, then processing
# a bit
drive_reveal(files, "parent")

# the "simple" cases of digging info out of `drive_resource`
drive_reveal(files, "trashed")
drive_reveal(files, "mime_type")
drive_reveal(files, "starred")
drive_reveal(files, "description")
drive_reveal(files, "version")
drive_reveal(files, "web_view_link")
drive_reveal(files, "modified_time")
drive_reveal(files, "created_time")
drive_reveal(files, "owned_by_me")
drive_reveal(files, "size")
drive_reveal(files, "quota_bytes_used")

# 'root' is a special file id that represents your My Drive root folder
drive_get(id = "root") |>
  drive_reveal("path")
}) # examplesIf