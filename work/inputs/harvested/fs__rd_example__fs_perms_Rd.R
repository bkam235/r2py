# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: fs_perms.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 15

suppressPackageStartupMessages(library(fs))
# Integer and numeric
fs_perms(420L)
fs_perms(c(511, 420))

# Octal
fs_perms("777")
fs_perms(c("777", "644"))

# Symbolic
fs_perms("a+rwx")
fs_perms(c("a+rwx", "u+rw,go+r"))

# Use the `&` and `|`operators to check for certain permissions
(fs_perms("777") & "u+r") == "u+r"