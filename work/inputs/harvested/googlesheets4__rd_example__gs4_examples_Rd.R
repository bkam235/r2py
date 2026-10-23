# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: gs4_examples.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 8

suppressPackageStartupMessages(library(googlesheets4))
if (gs4_has_token()) withAutoprint({ # examplesIf
gs4_examples()
gs4_examples("gap")

gs4_example("gapminder")
gs4_example("deaths")
}) # examplesIf