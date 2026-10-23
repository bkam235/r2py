# r2py crawler metadata
# package: xtable
# source_type: rd_example
# topic: print.xtable.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\help
# lines: 18

suppressPackageStartupMessages(library(xtable))
df <- data.frame(A = c(1.00123, 33.1, 6),
                 B = c(111111, 3333333, 3123.233))
## The following code gives the error
## formal argument "digits" matched by multiple actual arguments
## print(xtable(df, display = c("s","e","e")),
##       format.args = list(digits = 3, big.mark = " ", decimal.mark = ","))
## specify digits as argument to xtable instead
print(xtable(df, display = c("s","f","f"), digits = 4),
      format.args = list(big.mark = " ", decimal.mark = ","))
## The following code gives the error
## formal argument "format" matched by multiple actual arguments
## print(xtable(df, digits = 4),
##       format.args = list(format = c("s","e","e"),
##                          big.mark = " ", decimal.mark = ","))
## specify format using display argument in xtable
print(xtable(df, display = c("s","e","e"), digits = 4),
      format.args = list(big.mark = " ", decimal.mark = ","))