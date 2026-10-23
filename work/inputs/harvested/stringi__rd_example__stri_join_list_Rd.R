# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_join_list.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 23

suppressPackageStartupMessages(library(stringi))
stri_join_list(
   stri_extract_all_words(c('Lorem ipsum dolor sit amet.',
   'Spam spam bacon sausage and spam.')),
sep=', ')

stri_join_list(
   stri_extract_all_words(c('Lorem ipsum dolor sit amet.',
   'Spam spam bacon sausage and spam.')),
sep=', ', collapse='. ')

stri_join_list(
   stri_extract_all_regex(
      c('spam spam bacon', '123 456', 'spam 789 sausage'), '\\p{L}+'
   ),
sep=',')

stri_join_list(
   stri_extract_all_regex(
      c('spam spam bacon', '123 456', 'spam 789 sausage'), '\\p{L}+',
      omit_no_match=TRUE
   ),
sep=',', collapse='; ')