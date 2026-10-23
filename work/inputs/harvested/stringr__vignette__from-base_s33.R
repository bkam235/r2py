# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s33
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 19

suppressPackageStartupMessages(library(stringr))
name <- "Fred"
age <- 50
anniversary <- as.Date("1991-10-12")

# base
sprintf(
  "My name is %s my age next year is %s and my anniversary is %s.", 
  name,
  age + 1,
  format(anniversary, "%A, %B %d, %Y")
)

# stringr
str_glue(
  "My name is {name}, ",
  "my age next year is {age + 1}, ",
  "and my anniversary is {format(anniversary, '%A, %B %d, %Y')}."
)