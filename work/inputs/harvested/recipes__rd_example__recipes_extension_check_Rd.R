# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: recipes_extension_check.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 10

suppressPackageStartupMessages(library(recipes))
recipes_extension_check(
  pkg = "recipes"
)

recipes_extension_check(
  pkg = "recipes",
  exclude_steps = "step_testthat_helper",
  exclude_methods = c("required_pkgs")
)