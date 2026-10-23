# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s27
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 12

suppressPackageStartupMessages(library(stringr))
dog <- "The quick brown dog"

# base
toupper(dog)
tolower(dog)
tools::toTitleCase(dog)

# stringr
str_to_upper(dog)
str_to_lower(dog)
str_to_title(dog)