# r2py crawler metadata
# package: haven
# source_type: rd_example
# topic: as_factor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\haven\help
# lines: 18

suppressPackageStartupMessages(library(haven))
x <- labelled(sample(5, 10, replace = TRUE), c(Bad = 1, Good = 5))

# Default method uses values where available
as_factor(x)
# You can also extract just the labels
as_factor(x, levels = "labels")
# Or just the values
as_factor(x, levels = "values")
# Or combine value and label
as_factor(x, levels = "both")

# as_factor() will preserve SPSS missing values from values and ranges
y <- labelled_spss(1:10, na_values = c(2, 4), na_range = c(8, 10))
as_factor(y)
# use zap_missing() first to convert to NAs
zap_missing(y)
as_factor(zap_missing(y))