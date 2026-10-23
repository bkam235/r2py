# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 8

suppressPackageStartupMessages(library(stringr))
pattern <- "(..)\\1"
fruit %>% 
  str_subset(pattern)

fruit %>% 
  str_subset(pattern) %>% 
  str_match(pattern)