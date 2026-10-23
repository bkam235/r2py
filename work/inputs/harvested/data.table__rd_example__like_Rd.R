# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: like.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 6

suppressPackageStartupMessages(library(data.table))
DT = data.table(Name=c("Mary","George","Martha"), Salary=c(2,3,4))
DT[Name %like% "^Mar"]
DT[Name %ilike% "mar"]
DT[Name %flike% "Mar"]
DT[Name %plike% "(?=Ma)(?=.*y)"]