# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_rank.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 11

suppressPackageStartupMessages(library(stringi))
stri_rank(c('hladny', 'chladny'), locale='pl_PL')
stri_rank(c('hladny', 'chladny'), locale='sk_SK')

stri_rank("a" %s+% c(1, 100, 2, 101, 11, 10))  # lexicographic order
stri_rank("a" %s+% c(1, 100, 2, 101, 11, 10), numeric=TRUE)  # OK
stri_rank("a" %s+% c(0.25, 0.5, 1, -1, -2, -3), numeric=TRUE)  # incorrect

# Ordering a data frame with respect to two criteria:
X <- data.frame(a=c("b", NA, "b", "b", NA, "a", "a", "c"), b=runif(8))
X[order(stri_rank(X$a), X$b), ]