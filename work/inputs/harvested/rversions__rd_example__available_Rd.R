# r2py crawler metadata
# package: rversions
# source_type: rd_example
# topic: available.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rversions\help
# lines: 8

suppressPackageStartupMessages(library(rversions))
if (rversions:::is_online()) withAutoprint({ # examplesIf
available()
available("windows")
available("macos-arm64")
available("linux-gnu-ubuntu-24.04")
available("aarch64-unknown-linux-gnu-ubuntu-22.04")
}) # examplesIf