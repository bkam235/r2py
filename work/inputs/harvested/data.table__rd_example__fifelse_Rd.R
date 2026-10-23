# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: fifelse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 19

suppressPackageStartupMessages(library(data.table))
x = c(1:4, 3:2, 1:4)
fifelse(x > 2L, x, x - 1L)

# unlike ifelse, fifelse preserves attributes, taken from the 'yes' argument
dates = as.Date(c("2011-01-01","2011-01-02","2011-01-03","2011-01-04","2011-01-05"))
ifelse(dates == "2011-01-01", dates - 1, dates)
fifelse(dates == "2011-01-01", dates - 1, dates)
yes = factor(c("a","b","c"))
no = yes[1L]
ifelse(c(TRUE,FALSE,TRUE), yes, no)
fifelse(c(TRUE,FALSE,TRUE), yes, no)

# Example of using the 'na' argument
fifelse(test = c(-5L:5L < 0L, NA), yes = 1L, no = 0L, na = 2L)

# Example showing both 'yes' and 'no' arguments are evaluated, unlike ifelse
fifelse(1 == 1, print("yes"), print("no"))
ifelse(1 == 1, print("yes"), print("no"))