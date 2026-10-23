# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_about.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 9

suppressPackageStartupMessages(library(googledrive))
if (drive_has_token()) withAutoprint({ # examplesIf
drive_about()

# explore the export formats available for Drive files, by MIME type
about <- drive_about()
about[["exportFormats"]] |>
  purrr::map(unlist)
}) # examplesIf