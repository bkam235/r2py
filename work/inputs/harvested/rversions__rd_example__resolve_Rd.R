# r2py crawler metadata
# package: rversions
# source_type: rd_example
# topic: resolve.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rversions\help
# lines: 8

suppressPackageStartupMessages(library(rversions))
if (rversions:::is_online()) withAutoprint({ # examplesIf
resolve("release", "windows")
resolve("4.4", "windows-aarch64")
resolve("oldrel", "macos")
resolve("devel", "linux-gnu-ubuntu-24.04")
resolve("devel", "aarch64-unknown-linux-gnu-ubuntu-22.04")
}) # examplesIf