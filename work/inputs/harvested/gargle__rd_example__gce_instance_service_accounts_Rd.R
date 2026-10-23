# r2py crawler metadata
# package: gargle
# source_type: rd_example
# topic: gce_instance_service_accounts.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\help
# lines: 4

suppressPackageStartupMessages(library(gargle))
if (gargle:::is_gce()) withAutoprint({ # examplesIf
credentials_gce()
}) # examplesIf