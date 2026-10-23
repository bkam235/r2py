# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: order-radix.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 34

suppressPackageStartupMessages(library(vctrs))
if (FALSE) {

x <- round(sample(runif(5), 9, replace = TRUE), 3)
x <- c(x, NA)

vec_order_radix(x)
vec_sort_radix(x)
vec_sort_radix(x, direction = "desc")

# Can also handle data frames
df <- data.frame(g = sample(2, 10, replace = TRUE), x = x)
vec_order_radix(df)
vec_sort_radix(df)
vec_sort_radix(df, direction = "desc")

# For data frames, `direction` and `na_value` are allowed to be vectors
# with length equal to the number of columns in the data frame
vec_sort_radix(
  df,
  direction = c("desc", "asc"),
  na_value = c("largest", "smallest")
)

# Character vectors are ordered in the C locale, which orders capital letters
# below lowercase ones
y <- c("B", "A", "a")
vec_sort_radix(y)

# To order in a case-insensitive manner, provide a `chr_proxy_collate`
# function that transforms the strings to all lowercase
vec_sort_radix(y, chr_proxy_collate = tolower)

}