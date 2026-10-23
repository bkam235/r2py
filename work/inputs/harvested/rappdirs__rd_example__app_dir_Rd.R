# r2py crawler metadata
# package: rappdirs
# source_type: rd_example
# topic: app_dir.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rappdirs\help
# lines: 8

suppressPackageStartupMessages(library(rappdirs))
ggplot2_app <- app_dir("ggplot2", "hadley")
ggplot2_app$cache()
ggplot2_app$log()
ggplot2_app$data()
ggplot2_app$config()
ggplot2_app$site_config()
ggplot2_app$site_data()