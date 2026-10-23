# r2py crawler metadata
# package: DBI
# source_type: vignette
# topic: DBI-advanced_s17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\doc\DBI-advanced.R
# lines: 15

suppressPackageStartupMessages(library(DBI))
try({
withdraw_safely <- function(amount) {
  dbWithTransaction(con, {
    withdraw(amount)
    if (dbReadTable(con, "account")$amount < 0) {
      stop("Error: insufficient funds", call. = FALSE)
    }
  })
}

withdraw_safely(5000)
dbReadTable(con, "cash")
dbReadTable(con, "account")
})