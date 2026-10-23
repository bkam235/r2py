# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_subset.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 7

suppressPackageStartupMessages(library(stringi))
stri_subset_regex(c('stringi R', '123', 'ID456', ''), '^[0-9]+$')

x <- c('stringi R', '123', 'ID456', '')
`stri_subset_regex<-`(x, '[0-9]+$', negate=TRUE, value=NA)  # returns a copy
stri_subset_regex(x, '[0-9]+$') <- NA  # modifies `x` in-place
print(x)