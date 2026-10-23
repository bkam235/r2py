# r2py crawler metadata
# package: haven
# source_type: rd_example
# topic: zap_labels.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\haven\help
# lines: 16

suppressPackageStartupMessages(library(haven))
x1 <- labelled(1:5, c(good = 1, bad = 5))
x1
zap_labels(x1)

x2 <- labelled_spss(c(1:4, 9), c(good = 1, bad = 5), na_values = 9)
x2
zap_labels(x2)

# Keep the user defined missing values
zap_labels(x2, user_na = TRUE)

# zap_labels also works with data frames
df <- tibble::tibble(x1, x2)
df
zap_labels(df)