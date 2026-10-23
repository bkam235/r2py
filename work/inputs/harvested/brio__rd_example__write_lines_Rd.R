# r2py crawler metadata
# package: brio
# source_type: rd_example
# topic: write_lines.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\brio\help
# lines: 9

suppressPackageStartupMessages(library(brio))
tf <- tempfile()

write_lines(rownames(mtcars), tf)

# Write with Windows style line endings
write_lines(rownames(mtcars), tf, eol = "\r\n")

unlink(tf)