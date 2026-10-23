# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: print.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 17

suppressPackageStartupMessages(library(pROC))
data(aSAH)

# Print a roc object:
rocobj <- roc(aSAH$outcome, aSAH$s100b)
print(rocobj)

# Print a smoothed roc object
print(smooth(rocobj))

# implicit printing
 roc(aSAH$outcome, aSAH$s100b)

# Print an auc and a ci object, from the ROC object or calling
# the dedicated function:
print(rocobj$auc)
print(ci(rocobj))