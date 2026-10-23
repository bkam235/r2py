# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: impute.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 5

suppressPackageStartupMessages(library(e1071))
x<- matrix(1:10, ncol=2)
x[c(1,3,7)] <- NA
print(x)
print(impute(x))