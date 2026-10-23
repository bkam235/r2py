# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: hash.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 12

suppressPackageStartupMessages(library(rlang))
hash(c(1, 2, 3))
hash(mtcars)

authors <- file.path(R.home("doc"), "AUTHORS")
copying <- file.path(R.home("doc"), "COPYING")
hashes <- hash_file(c(authors, copying))
hashes

# If you need a single hash for multiple files,
# hash the result of `hash_file()`
hash(hashes)