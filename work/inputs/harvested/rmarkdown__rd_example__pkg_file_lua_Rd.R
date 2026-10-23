# r2py crawler metadata
# package: rmarkdown
# source_type: rd_example
# topic: pkg_file_lua.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rmarkdown\help
# lines: 5

suppressPackageStartupMessages(library(rmarkdown))
# list all Lua filters stored in the rmarkdown package
pkg_file_lua()
# get a specific filter
pkg_file_lua(c("pagebreak.lua", "latex_div.lua"))