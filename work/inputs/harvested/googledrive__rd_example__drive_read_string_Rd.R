# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_read_string.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 14

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
# comma-separated values --> data.frame or tibble
(chicken_csv <- drive_example_remote("chicken.csv"))
read.csv(text = chicken_csv |> drive_read_string())

# Google Doc --> character vector
(chicken_doc <- drive_example_remote("chicken_doc"))
chicken_doc |>
  # NOTE: we must specify an export MIME type
  drive_read_string(type = "text/plain") |>
  strsplit(split = "(\r\n|\r|\n)")
  (\(x) x[[1]])()
}) # examplesIf