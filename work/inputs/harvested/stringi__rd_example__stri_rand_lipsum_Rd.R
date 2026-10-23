# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_rand_lipsum.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 5

suppressPackageStartupMessages(library(stringi))
cat(sapply(
   stri_wrap(stri_rand_lipsum(10), 80, simplify=FALSE),
   stri_flatten, collapse='\n'), sep='\n\n')
cat(stri_rand_lipsum(10), sep='\n\n')