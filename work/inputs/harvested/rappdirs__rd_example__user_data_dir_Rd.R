# r2py crawler metadata
# package: rappdirs
# source_type: rd_example
# topic: user_data_dir.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rappdirs\help
# lines: 8

suppressPackageStartupMessages(library(rappdirs))
user_data_dir("rappdirs")

user_config_dir("rappdirs", roaming = TRUE, os = "win")
user_config_dir("rappdirs", roaming = FALSE, os = "win")
user_config_dir("rappdirs", os = "unix")
user_config_dir("rappdirs", os = "mac")
user_config_dir("rappdirs", version = "%p-platform/%v")