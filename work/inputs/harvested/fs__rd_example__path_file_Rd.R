# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: path_file.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 13

suppressPackageStartupMessages(library(fs))
path_file("dir/file.zip")

path_dir("dir/file.zip")

path_ext("dir/file.zip")

path_ext("file.tar.gz")

path_ext_remove("file.tar.gz")

# Only one level of extension is removed
path_ext_set(path_ext_remove("file.tar.gz"), "zip")