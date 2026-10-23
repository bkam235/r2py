# r2py crawler metadata
# package: memoise
# source_type: rd_example
# topic: cache_filesystem.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\memoise\help
# lines: 12

suppressPackageStartupMessages(library(memoise))
# Use with Dropbox

db <- cache_filesystem("~/Dropbox/.rcache")

mem_runif <- memoise(runif, cache = db)

# Use with Google Drive

gd <- cache_filesystem("~/Google Drive/.rcache")

mem_runif <- memoise(runif, cache = gd)