# r2py crawler metadata
# package: httpuv
# source_type: rd_example
# topic: runStaticServer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httpuv\help
# lines: 5

suppressPackageStartupMessages(library(httpuv))
if (interactive()) withAutoprint({ # examplesIf
website_dir <- system.file("example-static-site", package = "httpuv")
runStaticServer(dir = website_dir)
}) # examplesIf