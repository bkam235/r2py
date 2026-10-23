# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: are.paired.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 25

suppressPackageStartupMessages(library(pROC))
data(aSAH)
aSAH.copy <- aSAH

# artificially insert NAs for demonstration purposes
aSAH.copy$outcome[42] <- NA
aSAH.copy$s100b[24] <- NA
aSAH.copy$ndka[1:10] <- NA

# Call roc() on the whole data
roc1 <- roc(aSAH.copy$outcome, aSAH.copy$s100b)
roc2 <- roc(aSAH.copy$outcome, aSAH.copy$ndka)
# are.paired can still find that the curves were paired
are.paired(roc1, roc2) # TRUE

# Removing the NAs manually before passing to roc() un-pairs the ROC curves
nas <- is.na(aSAH.copy$outcome) | is.na(aSAH.copy$ndka)
roc2b <- roc(aSAH.copy$outcome[!nas], aSAH.copy$ndka[!nas])
are.paired(roc1, roc2b) # FALSE

# Getting the two paired ROC curves with additional smoothing and ci options
roc2$ci <- ci(roc2)
paired <- are.paired(smooth(roc1), roc2, return.paired.rocs=TRUE, reuse.ci=TRUE)
paired.roc1 <- attr(paired, "roc1")
paired.roc2 <- attr(paired, "roc2")