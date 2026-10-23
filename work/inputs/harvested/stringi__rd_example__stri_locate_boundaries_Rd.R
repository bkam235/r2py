# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_locate_boundaries.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 8

suppressPackageStartupMessages(library(stringi))
test <- 'The\u00a0above-mentioned    features are very useful. Spam, spam, eggs, bacon, and spam.'
stri_locate_all_words(test)
stri_locate_all_boundaries(
    'Mr. Jones and Mrs. Brown are very happy. So am I, Prof. Smith.',
    type='sentence',
    locale='en_US@ss=standard' # ICU >= 56 only
)