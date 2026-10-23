# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-joins_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-joins.R
# lines: 9

suppressPackageStartupMessages(library(data.table))
Products = rowwiseDT(
  id=,        name=, price=,   unit=, type=,
   1L,     "banana",   0.63,  "unit", "natural",
   2L,    "carrots",   0.89,    "lb", "natural",
   3L,    "popcorn",   2.99,  "unit", "processed",
   4L,       "soda",   1.49, "ounce", "processed",
   NA, "toothpaste",   2.99,  "unit", "processed"
)