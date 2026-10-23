# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: has.partial.auc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 17

suppressPackageStartupMessages(library(pROC))
data(aSAH)

# Full AUC
roc1 <- roc(aSAH$outcome, aSAH$s100b)
has.partial.auc(roc1)
has.partial.auc(auc(roc1))
has.partial.auc(smooth(roc1))

# Partial AUC
roc2 <- roc(aSAH$outcome, aSAH$s100b, partial.auc = c(1, 0.9))
has.partial.auc(roc2)
has.partial.auc(smooth(roc2))

# No AUC
roc3 <- roc(aSAH$outcome, aSAH$s100b, auc = FALSE)
has.partial.auc(roc3)