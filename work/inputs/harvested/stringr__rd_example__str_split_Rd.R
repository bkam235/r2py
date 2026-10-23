# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: str_split.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 27

suppressPackageStartupMessages(library(stringr))
fruits <- c(
  "apples and oranges and pears and bananas",
  "pineapples and mangos and guavas"
)

str_split(fruits, " and ")
str_split(fruits, " and ", simplify = TRUE)

# If you want to split a single string, use `str_split_1`
str_split_1(fruits[[1]], " and ")

# Specify n to restrict the number of possible matches
str_split(fruits, " and ", n = 3)
str_split(fruits, " and ", n = 2)
# If n greater than number of pieces, no padding occurs
str_split(fruits, " and ", n = 5)

# Use fixed to return a character matrix
str_split_fixed(fruits, " and ", 3)
str_split_fixed(fruits, " and ", 4)

# str_split_i extracts only a single piece from a string
str_split_i(fruits, " and ", 1)
str_split_i(fruits, " and ", 4)
# use a negative number to select from the end
str_split_i(fruits, " and ", -1)