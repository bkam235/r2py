# r2py crawler metadata
# package: pkgdown
# source_type: vignette
# topic: how-to-update-released-site_chunk5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pkgdown\doc\how-to-update-released-site.Rmd
# lines: 15

suppressPackageStartupMessages(library(pkgdown))
files <- c(
  # overall site config
  "_pkgdown.yml",
  # the workflow that builds the site
  ".github/workflows/pkgdown.yaml",
  # readme and vignettes
  "README.md", "vignettes",
  # logo and favicon
  "man/figures/", "pkgdown/",
  # Author metadata and Config/Needs/Website
  "DESCRIPTION"
)

glue::glue("git checkout main -- {files}")