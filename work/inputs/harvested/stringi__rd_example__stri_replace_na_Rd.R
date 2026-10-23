# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_replace_na.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 5

suppressPackageStartupMessages(library(stringi))
x <- c('test', NA)
stri_paste(x, 1:2)                           # 'test1' NA
paste(x, 1:2)                                # 'test 1' 'NA 2'
stri_paste(stri_replace_na(x), 1:2, sep=' ') # 'test 1' 'NA 2'