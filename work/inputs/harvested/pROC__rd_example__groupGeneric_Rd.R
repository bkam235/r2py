# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: groupGeneric.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 20

suppressPackageStartupMessages(library(pROC))
data(aSAH)

# Create a roc object:
aucobj1 <- auc(roc(aSAH$outcome, aSAH$s100b))
aucobj2 <- auc(roc(aSAH$outcome, aSAH$wfns))

# Math
sqrt(aucobj1)
round(aucobj2, digits=1)

# Ops
aucobj1 * 2
2 * aucobj2
aucobj1 + aucobj2

# With CI
ciaucobj <- ci(aucobj1)
ciaucobj * 2
sqrt(ciaucobj)