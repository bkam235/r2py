# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 7

suppressPackageStartupMessages(library(stringr))
# base 
loc <- gregexpr(pattern = "a", text = fruit, fixed = TRUE)
sapply(loc, function(x) length(attr(x, "match.length")))

# stringr
str_count(fruit, pattern = "a")