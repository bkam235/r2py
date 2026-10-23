# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-joins_s39
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-joins.R
# lines: 9

suppressPackageStartupMessages(library(data.table))
ProductPriceHistory = data.table(
  product_id = rep(1:2, each = 3),
  date = rep(as.IDate(c("2024-01-01", "2024-02-01", "2024-03-01")), 2),
  price = c(0.59, 0.63, 0.65,  # Banana prices
            0.79, 0.89, 0.99)  # Carrot prices
)

ProductPriceHistory