# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_envvar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 7

suppressPackageStartupMessages(library(withr))
with_envvar(new = c("GITHUB_PAT" = "abcdef"), Sys.getenv("GITHUB_PAT"))

# with_envvar unsets variables after usage
Sys.getenv("TEMP_SECRET")
with_envvar(new = c("TEMP_SECRET" = "secret"), Sys.getenv("TEMP_SECRET"))
Sys.getenv("TEMP_SECRET")