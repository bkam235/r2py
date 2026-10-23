# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: github_releases.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
if (interactive()) {
xfun::github_releases("yihui/litedown")
xfun::github_releases("gohugoio/hugo", "latest")
}