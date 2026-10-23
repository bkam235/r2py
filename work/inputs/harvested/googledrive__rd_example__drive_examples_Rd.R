# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_examples.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 10

suppressPackageStartupMessages(library(googledrive))
drive_examples_local() |> basename()
drive_examples_local("chicken") |> basename()
drive_example_local("imdb")

if (drive_has_token()) withAutoprint({ # examplesIf
drive_examples_remote()
drive_examples_remote("chicken")
drive_example_remote("chicken_doc")
}) # examplesIf