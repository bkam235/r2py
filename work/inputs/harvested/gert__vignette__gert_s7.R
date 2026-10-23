# r2py crawler metadata
# package: gert
# source_type: vignette
# topic: gert_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\doc\gert.R
# lines: 5

suppressPackageStartupMessages(library(gert))
r2 <- file.path(tempdir(), "repo_ddd")
dir.create(r2)

git_init(r2)