# r2py crawler metadata
# package: usethis
# source_type: rd_example
# topic: browse-this.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\usethis\help
# lines: 11

suppressPackageStartupMessages(library(usethis))
# works on the active project
# browse_project()

browse_package("httr")
browse_github("gh")
browse_github_issues("fs")
browse_github_issues("fs", 1)
browse_github_pulls("curl")
browse_github_pulls("curl", 183)
browse_cran("MASS")