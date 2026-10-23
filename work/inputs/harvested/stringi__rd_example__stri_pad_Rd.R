# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_pad.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 9

suppressPackageStartupMessages(library(stringi))
stri_pad_left('stringi', 10, pad='#')
stri_pad_both('stringi', 8:12, pad='*')
# center on screen:
cat(stri_pad_both(c('the', 'string', 'processing', 'package'),
   getOption('width')*0.9), sep='\n')
cat(stri_pad_both(c('\ud6c8\ubbfc\uc815\uc74c', # takes width into account
   stri_trans_nfkd('\ud6c8\ubbfc\uc815\uc74c'), 'abcd'),
   width=10), sep='\n')