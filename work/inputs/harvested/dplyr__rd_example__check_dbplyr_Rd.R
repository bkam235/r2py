# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: check_dbplyr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 5

suppressPackageStartupMessages(library(dplyr))
if (requireNamespace("dbplyr", quietly = TRUE)) withAutoprint({ # examplesIf
wrap_dbplyr_obj("build_sql")
wrap_dbplyr_obj("base_agg")
}) # examplesIf