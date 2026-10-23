# r2py crawler metadata
# package: haven
# source_type: rd_example
# topic: labelled.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\haven\help
# lines: 28

suppressPackageStartupMessages(library(haven))
s1 <- labelled(c("M", "M", "F"), c(Male = "M", Female = "F"))
s2 <- labelled(c(1, 1, 2), c(Male = 1, Female = 2))
s3 <- labelled(
  c(1, 1, 2),
  c(Male = 1, Female = 2),
  label = "Assigned sex at birth"
)

# Unfortunately it's not possible to make as.factor work for labelled objects
# so instead use as_factor. This works for all types of labelled vectors.
as_factor(s1)
as_factor(s1, levels = "values")
as_factor(s2)

# Other statistical software supports multiple types of missing values
s3 <- labelled(
  c("M", "M", "F", "X", "N/A"),
  c(Male = "M", Female = "F", Refused = "X", "Not applicable" = "N/A")
)
s3
as_factor(s3)

# Often when you have a partially labelled numeric vector, labelled values
# are special types of missing. Use zap_labels to replace labels with missing
# values
x <- labelled(c(1, 2, 1, 2, 10, 9), c(Unknown = 9, Refused = 10))
zap_labels(x)