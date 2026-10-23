# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: geom_polygon_auc.roc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 17

suppressPackageStartupMessages(library(pROC))
# Create a ROC curve:
data(aSAH)
roc.s100b <- roc(aSAH$outcome, aSAH$s100b)
roc.s100b.percent <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)

ggroc(roc.s100b) + geom_polygon_auc(roc.s100b$auc)

# legacy.axes must be repeated
ggroc(roc.s100b.percent, legacy.axes=TRUE) + geom_polygon_auc(roc.s100b.percent, legacy.axes=TRUE)

# Partial AUCs
auc.s100b.partial.sp <- auc(roc.s100b, partial.auc = c(0.9, 1))
auc.s100b.partial.se <- auc(roc.s100b, partial.auc = c(0.8, 0.9), partial.auc.focus="se")

ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.sp)
ggroc(roc.s100b) + geom_polygon_auc(auc.s100b.partial.se)