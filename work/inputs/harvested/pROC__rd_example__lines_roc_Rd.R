# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: lines.roc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 18

suppressPackageStartupMessages(library(pROC))
# Create a few ROC curves:
data(aSAH)
roc.s100b <- roc(aSAH$outcome, aSAH$s100b)
roc.wfns <- roc(aSAH$outcome, aSAH$wfns)

# We need a plot to be ready
plot(roc.s100b, type = "n") # but don't actually plot the curve

# Add the line
lines(roc.s100b, type="b", pch=21, col="blue", bg="grey")

# Add the line of an other ROC curve
lines(roc.wfns, type="o", pch=19, col="red")


# Without using 'lines':
rocobj <- plot.roc(aSAH$outcome, aSAH$s100b, type="b", pch=21, col="blue", bg="grey")