# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 16

suppressPackageStartupMessages(library(curl))
con <- curl("https://hb.cran.dev/get")
open(con)

# Get 3 lines
out <- readLines(con, n = 3)
cat(out, sep = "\n")

# Get 3 more lines
out <- readLines(con, n = 3)
cat(out, sep = "\n")

# Get remaining lines
out <- readLines(con)
close(con)
cat(out, sep = "\n")