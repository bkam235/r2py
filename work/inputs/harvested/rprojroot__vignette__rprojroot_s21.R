# r2py crawler metadata
# package: rprojroot
# source_type: vignette
# topic: rprojroot_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rprojroot\doc\rprojroot.R
# lines: 6

suppressPackageStartupMessages(library(rprojroot))
has_license <- has_file("LICENSE")
has_license

is_projecttemplate_project <- has_file("config/global.dcf", "^version: ")
is_projecttemplate_project