# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: path_select_components.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 10

suppressPackageStartupMessages(library(fs))
path <- fs::path("some", "simple", "path", "to", "a", "file.txt")

path_select_components(path, 1:3)

path_select_components(path, 1:3, "end")

path_select_components(path, -1, "end")

path_select_components(path, 6)