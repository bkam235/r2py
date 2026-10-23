# r2py crawler metadata
# package: utf8
# source_type: rd_example
# topic: output_utf8.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\utf8\help
# lines: 21

suppressPackageStartupMessages(library(utf8))
# test whether ANSI style escapes or UTF-8 output are supported
cat("ANSI:", output_ansi(), "\n")
cat("UTF8:", output_utf8(), "\n")

# switch to C locale
Sys.setlocale("LC_CTYPE", "C")
cat("ANSI:", output_ansi(), "\n")
cat("UTF8:", output_utf8(), "\n")

# switch to native locale
Sys.setlocale("LC_CTYPE", "")

tmp <- tempfile()
sink(tmp) # redirect output to a file
cat("ANSI:", output_ansi(), "\n")
cat("UTF8:", output_utf8(), "\n")
sink() # restore stdout

# inspect the output
readLines(tmp)