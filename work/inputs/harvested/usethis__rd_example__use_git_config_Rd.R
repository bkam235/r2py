# r2py crawler metadata
# package: usethis
# source_type: rd_example
# topic: use_git_config.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\usethis\help
# lines: 10

suppressPackageStartupMessages(library(usethis))
# set the user's global user.name and user.email
use_git_config(user.name = "Jane", user.email = "jane@example.org")

# set the user.name and user.email locally, i.e. for current repo/project
use_git_config(
  scope = "project",
  user.name = "Jane",
  user.email = "jane@example.org"
)