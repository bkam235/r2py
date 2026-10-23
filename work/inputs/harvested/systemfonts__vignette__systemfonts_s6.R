# r2py crawler metadata
# package: systemfonts
# source_type: vignette
# topic: systemfonts_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\doc\systemfonts.R
# lines: 4

suppressPackageStartupMessages(library(systemfonts))
all_fonts <- systemfonts::system_fonts()
all_fonts <- all_fonts[!grepl("^/Users", all_fonts$path),]
rmarkdown::paged_table(all_fonts)