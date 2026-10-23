# r2py crawler metadata
# package: rversions
# source_type: rd_example
# topic: rtools_versions.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rversions\help
# lines: 5

suppressPackageStartupMessages(library(rversions))
if (rversions:::is_online()) withAutoprint({ # examplesIf
rtools_versions()
rtools_versions("aarch64")
}) # examplesIf