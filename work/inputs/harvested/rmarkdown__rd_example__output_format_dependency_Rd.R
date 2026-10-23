# r2py crawler metadata
# package: rmarkdown
# source_type: rd_example
# topic: output_format_dependency.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rmarkdown\help
# lines: 20

suppressPackageStartupMessages(library(rmarkdown))
# Implicitly add lua filters from within a chunk
# This relies on (implicit) printing of the dependency in a chunk via
# knitr::knit_print()`
output_format_dependency(
  "lua_filter1",
  pandoc = list(lua_filters = "example1.lua")
)

# Explicitly add lua filters from within a chunk
knitr::knit_meta_add(list(output_format_dependency(
  "lua_filter2",
  pandoc = list(lua_filters = "example2.lua")
)))

# List the available dependencies
# Note that the list may include dependencies with duplicated names. In that
# case, the first one is merged to the output format and the others are
# discarded.
str(knitr::knit_meta("output_format_dependency", clean = FALSE))