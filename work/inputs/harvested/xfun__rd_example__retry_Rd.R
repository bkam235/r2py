# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: retry.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
if (interactive()) {
# read the GitHub releases info of the repo yihui/xfun
xfun::retry(xfun::github_releases, "yihui/xfun")
}