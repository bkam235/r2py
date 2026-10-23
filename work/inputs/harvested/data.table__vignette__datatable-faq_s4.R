# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-faq_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-faq.R
# lines: 4

suppressPackageStartupMessages(library(data.table))
DF = data.frame(x = 1:3, y = 4:6, z = 7:9)
DF
DF[ , c("y", "z")]