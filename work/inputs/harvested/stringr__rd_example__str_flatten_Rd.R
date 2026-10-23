# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: str_flatten.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 18

suppressPackageStartupMessages(library(stringr))
str_flatten(letters)
str_flatten(letters, "-")

str_flatten(letters[1:3], ", ")

# Use last to customise the last component
str_flatten(letters[1:3], ", ", " and ")

# this almost works if you want an Oxford (aka serial) comma
str_flatten(letters[1:3], ", ", ", and ")

# but it will always add a comma, even when not necessary
str_flatten(letters[1:2], ", ", ", and ")

# str_flatten_comma knows how to handle the Oxford comma
str_flatten_comma(letters[1:3], ", and ")
str_flatten_comma(letters[1:2], ", and ")