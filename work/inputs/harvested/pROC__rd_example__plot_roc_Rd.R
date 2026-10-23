# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: plot.roc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 39

suppressPackageStartupMessages(library(pROC))
# Create a few ROC curves:
data(aSAH)
roc.s100b <- roc(aSAH$outcome, aSAH$s100b)
roc.wfns <- roc(aSAH$outcome, aSAH$wfns)
roc.ndka <- roc(aSAH$outcome, aSAH$wfns)

# Simple example:
plot(roc.s100b)

# Add a smoothed ROC:
plot(smooth(roc.s100b), add=TRUE, col="blue")
legend("bottomright", legend=c("Empirical", "Smoothed"),
       col=c(par("fg"), "blue"), lwd=2)

# With more options:
plot(roc.s100b, print.auc=TRUE, auc.polygon=TRUE, grid=c(0.1, 0.2),
     grid.col=c("green", "red"), max.auc.polygon=TRUE,
     auc.polygon.col="lightblue", print.thres=TRUE)

# To plot a different partial AUC, we need to ignore the existing value
# with reuse.auc=FALSE:
plot(roc.s100b, print.auc=TRUE, auc.polygon=TRUE, partial.auc=c(1, 0.8),
     partial.auc.focus="se", grid=c(0.1, 0.2), grid.col=c("green", "red"),
     max.auc.polygon=TRUE, auc.polygon.col="lightblue", 
     print.thres=TRUE, print.thres.adj = c(1, -1),
     reuse.auc=FALSE)

# Add a second ROC curve to the previous plot:
plot(roc.wfns, add=TRUE)

# Plot some thresholds, add them to the same plot
plot(roc.ndka, print.thres="best", print.thres.best.method="youden")
plot(roc.ndka, print.thres="best", print.thres.best.method="closest.topleft",
                                   add = TRUE)
plot(roc.ndka, print.thres="best", print.thres.best.method="youden",
                                   print.thres.best.weights=c(50, 0.2),
                                   print.thres.adj = c(1.1, 1.25),
                                   add = TRUE)