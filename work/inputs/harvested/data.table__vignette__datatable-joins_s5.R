# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-joins_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-joins.R
# lines: 14

suppressPackageStartupMessages(library(data.table))
set.seed(2156)

# NB: Jan 8, 2024 is a Monday.
receipt_dates = seq(from=as.IDate("2024-01-08"), length.out=10L, by="week")

ProductReceived = data.table(
  id=1:10, # unique identifier for an supply transaction
  date=receipt_dates,
  product_id=sample(c(NA, 1:3, 6L), size=10L, replace=TRUE), # NB: product '6' is not recorded in Products above.
  count=sample(c(50L, 100L, 150L), size=10L, replace=TRUE)
)

ProductReceived