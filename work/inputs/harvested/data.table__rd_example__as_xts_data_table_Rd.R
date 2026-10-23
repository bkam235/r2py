# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: as.xts.data.table.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 10

suppressPackageStartupMessages(library(data.table))
if (requireNamespace("xts", quietly = TRUE)) {
  sample.dt <- data.table(date = as.Date((Sys.Date()-999):Sys.Date(),origin="1970-01-01"),
                          quantity = sample(10:50,1000,TRUE),
                          value = sample(100:1000,1000,TRUE))
  # print data.table
  print(sample.dt)
  # print head of xts
  print(head(as.xts.data.table(sample.dt))) # xts might not be attached on search path
}