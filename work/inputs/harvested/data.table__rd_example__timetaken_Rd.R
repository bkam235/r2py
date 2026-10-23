# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: timetaken.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 4

suppressPackageStartupMessages(library(data.table))
started.at=proc.time()
Sys.sleep(1)
cat("Finished in",timetaken(started.at),"\n")