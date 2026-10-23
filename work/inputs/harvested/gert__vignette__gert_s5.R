# r2py crawler metadata
# package: gert
# source_type: vignette
# topic: gert_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\doc\gert.R
# lines: 6

suppressPackageStartupMessages(library(gert))
(path <- file.path(tempdir(), "aaa", "bbb", "repo_ccc"))
dir.exists(path)

(r <- git_init(path))
dir.exists(path)