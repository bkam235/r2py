# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-programming_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-programming.R
# lines: 15

suppressPackageStartupMessages(library(data.table))
substitute(    # base R behaviour
  rank(input, ties.method = ties),
  env = list(input = as.name("Sepal.Width"), ties = "first")
)

substitute2(   # mimicking base R's "substitute" using "I"
  rank(input, ties.method = ties),
  env = I(list(input = as.name("Sepal.Width"), ties = "first"))
)

substitute2(   # only particular elements of env are used "AsIs"
  rank(input, ties.method = ties),
  env = list(input = "Sepal.Width", ties = I("first"))
)