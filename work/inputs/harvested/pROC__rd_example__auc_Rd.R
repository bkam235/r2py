# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: auc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 10

suppressPackageStartupMessages(library(pROC))
# Create a ROC curve:
data(aSAH)
roc.s100b <- roc(aSAH$outcome, aSAH$s100b)

# Get the full AUC
auc(roc.s100b)

# Get the partial AUC:
auc(roc.s100b, partial.auc=c(1, .8), partial.auc.focus="se", partial.auc.correct=TRUE)