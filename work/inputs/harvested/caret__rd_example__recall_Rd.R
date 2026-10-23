# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: recall.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 27

suppressPackageStartupMessages(library(caret))
###################
## Data in Table 2 of Powers (2007)

lvs <- c("Relevant", "Irrelevant")
tbl_2_1_pred <- factor(rep(lvs, times = c(42, 58)), levels = lvs)
tbl_2_1_truth <- factor(c(rep(lvs, times = c(30, 12)),
                          rep(lvs, times = c(30, 28))),
                        levels = lvs)
tbl_2_1 <- table(tbl_2_1_pred, tbl_2_1_truth)

precision(tbl_2_1)
precision(data = tbl_2_1_pred, reference = tbl_2_1_truth, relevant = "Relevant")
recall(tbl_2_1)
recall(data = tbl_2_1_pred, reference = tbl_2_1_truth, relevant = "Relevant")


tbl_2_2_pred <- factor(rep(lvs, times = c(76, 24)), levels = lvs)
tbl_2_2_truth <- factor(c(rep(lvs, times = c(56, 20)),
                          rep(lvs, times = c(12, 12))),
                        levels = lvs)
tbl_2_2 <- table(tbl_2_2_pred, tbl_2_2_truth)

precision(tbl_2_2)
precision(data = tbl_2_2_pred, reference = tbl_2_2_truth, relevant = "Relevant")
recall(tbl_2_2)
recall(data = tbl_2_2_pred, reference = tbl_2_2_truth, relevant = "Relevant")