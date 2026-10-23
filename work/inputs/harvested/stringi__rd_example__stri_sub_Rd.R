# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_sub.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 17

suppressPackageStartupMessages(library(stringi))
s <- c("spam, spam, bacon, and spam", "eggs and spam")
stri_sub(s, from=-4)
stri_sub(s, from=1, length=c(10, 4))
(stri_sub(s, 1, 4) <- 'stringi')

x <- c('12 3456 789', 'abc', '', NA, '667')
stri_sub(x, stri_locate_first_regex(x, '[0-9]+')) # see stri_extract_first
stri_sub(x, stri_locate_last_regex(x, '[0-9]+'))  # see stri_extract_last

stri_sub_replace(x, stri_locate_first_regex(x, '[0-9]+'),
    omit_na=TRUE, replacement='***') # see stri_replace_first
stri_sub_replace(x, stri_locate_last_regex(x, '[0-9]+'),
    omit_na=TRUE, replacement='***') # see stri_replace_last


x |> stri_sub_replace(1, 5, replacement='new_substring')