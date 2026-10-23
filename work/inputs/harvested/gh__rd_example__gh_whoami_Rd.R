# r2py crawler metadata
# package: gh
# source_type: rd_example
# topic: gh_whoami.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gh\help
# lines: 11

suppressPackageStartupMessages(library(gh))
if (identical(Sys.getenv("IN_PKGDOWN"), "true")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
gh_whoami()
}) # examplesIf
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
## explicit token + use with GitHub Enterprise
gh_whoami(
  .token = "8c70fd8419398999c9ac5bacf3192882193cadf2",
  .api_url = "https://github.foobar.edu/api/v3"
)
}) # examplesIf