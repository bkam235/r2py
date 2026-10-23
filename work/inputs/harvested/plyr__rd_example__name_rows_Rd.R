# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: name_rows.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 8

suppressPackageStartupMessages(library(plyr))
name_rows(mtcars)
name_rows(name_rows(mtcars))

df <- data.frame(a = sample(10))
arrange(df, a)
arrange(name_rows(df), a)
name_rows(arrange(name_rows(df), a))