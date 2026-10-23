# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: plot.ci.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 34

suppressPackageStartupMessages(library(pROC))
data(aSAH)

# Start a ROC plot
rocobj <- plot.roc(aSAH$outcome, aSAH$s100b)
plot(rocobj)
# Thresholds
ci.thresolds.obj <- ci.thresholds(rocobj)
plot(ci.thresolds.obj)
# Specificities
plot(rocobj) # restart a new plot
ci.sp.obj <- ci.sp(rocobj, boot.n=500)
plot(ci.sp.obj)
# Sensitivities
plot(rocobj) # restart a new plot
ci.se.obj <- ci(rocobj, of="se", boot.n=500)
plot(ci.se.obj)

# Plotting a shape. We need more
ci.sp.obj <- ci.sp(rocobj, sensitivities=seq(0, 1, .01), boot.n=100)
plot(rocobj) # restart a new plot
plot(ci.sp.obj, type="shape", col="blue")

# Direct syntax (response, predictor):
plot.roc(aSAH$outcome, aSAH$s100b,
         ci=TRUE, of="thresholds")

# CI of a PR curve
co <- coords(rocobj, x = "all", input="recall", ret=c("recall", "precision"))
ci <- ci.coords(rocobj, x = seq(0, 1, .1), input="recall", ret="precision")
plot(co, type="l", ylim = c(0, 1))
plot(ci, type="shape")
plot(ci, type="bars")
lines(co)