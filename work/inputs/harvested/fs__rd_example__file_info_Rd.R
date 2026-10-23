# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: file_info.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 12

suppressPackageStartupMessages(library(fs))
.old_wd <- setwd(tempdir())
write.csv(mtcars, "mtcars.csv")
file_info("mtcars.csv")

# Files in the working directory modified more than 20 days ago
files <- file_info(dir_ls())
files$path[difftime(Sys.time(), files$modification_time, units = "days") > 20]

# Cleanup
file_delete("mtcars.csv")
setwd(.old_wd)