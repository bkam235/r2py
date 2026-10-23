# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: nullModel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 8

suppressPackageStartupMessages(library(caret))
outcome <- factor(sample(letters[1:2],
                         size = 100,
                         prob = c(.1, .9),
                         replace = TRUE))
useless <- nullModel(y = outcome)
useless
predict(useless, matrix(NA, nrow = 10))