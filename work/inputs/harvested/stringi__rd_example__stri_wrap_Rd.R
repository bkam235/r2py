# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_wrap.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 8

suppressPackageStartupMessages(library(stringi))
s <- stri_paste(
   'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Proin ',
   'nibh augue, suscipit a, scelerisque sed, lacinia in, mi. Cras vel ',
   'lorem. Etiam pellentesque aliquet tellus.')
cat(stri_wrap(s, 20, 0.0), sep='\n') # greedy
cat(stri_wrap(s, 20, 2.0), sep='\n') # dynamic
cat(stri_pad(stri_wrap(s), side='both'), sep='\n')