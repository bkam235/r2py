# r2py crawler metadata
# package: gert
# source_type: rd_example
# topic: git_repo.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\help
# lines: 22

suppressPackageStartupMessages(library(gert))
# directory does not yet exist
r <- tempfile(pattern = "gert")
git_init(r)
git_find(r)

# create a child directory, then a grandchild, then search
r_grandchild_dir <- file.path(r, "aaa", "bbb")
dir.create(r_grandchild_dir, recursive = TRUE)
git_find(r_grandchild_dir)

# cleanup
unlink(r, recursive = TRUE)

# directory exists but is empty
r <- tempfile(pattern = "gert")
dir.create(r)
git_init(r)
git_find(r)

# cleanup
unlink(r, recursive = TRUE)