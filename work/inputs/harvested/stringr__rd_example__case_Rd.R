# r2py crawler metadata
# package: stringr
# source_type: rd_example
# topic: case.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\help
# lines: 10

suppressPackageStartupMessages(library(stringr))
dog <- "The quick brown dog"
str_to_upper(dog)
str_to_lower(dog)
str_to_title(dog)
str_to_sentence("the quick brown dog")

# Locale matters!
str_to_upper("i") # English
str_to_upper("i", "tr") # Turkish