# r2py crawler metadata
# package: gert
# source_type: rd_example
# topic: git_open.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\help
# lines: 10

suppressPackageStartupMessages(library(gert))
r <- tempfile(pattern = "gert")
git_init(r)
r_ptr <- git_open(r)
r_ptr
git_open(r_ptr)
git_info(r)

# cleanup
unlink(r, recursive = TRUE)