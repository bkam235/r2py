# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: path_expand.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 11

suppressPackageStartupMessages(library(fs))
# Expand a path
path_expand("~/bin")

# You can use `path_home()` without arguments to see what is being used as
# the home diretory.
path_home()
path_home("R")

# This will likely differ from the above on Windows
path_home_r()