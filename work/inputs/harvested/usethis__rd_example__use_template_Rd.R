# r2py crawler metadata
# package: usethis
# source_type: rd_example
# topic: use_template.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\usethis\help
# lines: 7

suppressPackageStartupMessages(library(usethis))
# Note: running this will write `NEWS.md` to your working directory
  use_template(
    template = "NEWS.md",
    data = list(Package = "acme", Version = "1.2.3"),
    package = "usethis"
  )