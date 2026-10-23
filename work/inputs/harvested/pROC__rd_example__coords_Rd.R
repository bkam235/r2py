# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: coords.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 63

suppressPackageStartupMessages(library(pROC))
# Create a ROC curve:
data(aSAH)
roc.s100b <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)

# Get the coordinates of S100B threshold 0.55
coords(roc.s100b, 0.55)

# Get the coordinates at 50% sensitivity
coords(roc=roc.s100b, x=50, input="sensitivity")
# Can be abbreviated:
coords(roc.s100b, 50, "se")

# Works with smoothed ROC curves
coords(smooth(roc.s100b), 90, "specificity")

# Get the sensitivities for all thresholds
cc <- coords(roc.s100b, "all", ret="sensitivity")
print(cc$sensitivity)

# Get the best threshold
coords(roc.s100b, "best", ret="threshold")

# Get the best threshold according to different methods
roc.ndka <- roc(aSAH$outcome, aSAH$ndka, percent=TRUE)
coords(roc.ndka, "best", ret="threshold", 
       best.method="youden") # default
coords(roc.ndka, "best", ret="threshold", 
       best.method="closest.topleft")

# and with different weights
coords(roc.ndka, "best", ret="threshold", 
       best.method="youden", best.weights=c(50, 0.2))
coords(roc.ndka, "best", ret="threshold", 
       best.method="closest.topleft", best.weights=c(5, 0.2))
       
# This is available with the plot.roc function too:
plot(roc.ndka, print.thres="best", print.thres.best.method="youden",
                                 print.thres.best.weights=c(50, 0.2)) 

# Return more values:
coords(roc.s100b, "best", ret=c("threshold", "specificity", "sensitivity", "accuracy",
                           "precision", "recall"))

# Return all values
coords(roc.s100b, "best", ret = "all")
                           
# You can use coords to plot for instance a sensitivity + specificity vs. cut-off diagram
plot(specificity + sensitivity ~ threshold, 
     coords(roc.ndka, "all"), 
     type = "l", log="x", 
     subset = is.finite(threshold))

# Plot the Precision-Recall curve
plot(precision ~ recall, 
     coords(roc.ndka, "all", ret = c("recall", "precision")),
     type="l", ylim = c(0, 100))

# Alternatively plot the curve with TPR and FPR instead of SE/SP 
# (identical curve, only the axis change)
plot(tpr ~ fpr, 
     coords(roc.ndka, "all", ret = c("tpr", "fpr")),
     type="l")