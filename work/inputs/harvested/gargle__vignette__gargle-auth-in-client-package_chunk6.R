# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: gargle-auth-in-client-package_chunk6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\gargle-auth-in-client-package.Rmd
# lines: 8

suppressPackageStartupMessages(library(gargle))
#| eval: false
library(googledrive)

drive_auth_configure(api_key = "123456789")

drive_api_key()
#> "123456789"