# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: ggroc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 47

suppressPackageStartupMessages(library(pROC))
# Create a basic roc object
data(aSAH)
rocobj <- roc(aSAH$outcome, aSAH$s100b)
rocobj2 <- roc(aSAH$outcome, aSAH$wfns)

if (require(ggplot2)) {
g <- ggroc(rocobj)
g
# with additional aesthetics:
ggroc(rocobj, alpha = 0.5, colour = "red", linetype = 2, size = 2)

# You can then your own theme, etc.
g + theme_minimal() + ggtitle("My ROC curve") + 
    geom_segment(aes(x = 1, xend = 0, y = 0, yend = 1), color="grey", linetype="dashed")

# And change axis labels to FPR/FPR
gl <- ggroc(rocobj, legacy.axes = TRUE)
gl
gl + xlab("FPR") + ylab("TPR") + 
    geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="darkgrey", linetype="dashed")

# Multiple curves:
g2 <- ggroc(list(s100b=rocobj, wfns=rocobj2, ndka=roc(aSAH$outcome, aSAH$ndka)))
g2

# This is equivalent to using roc.formula:
roc.list <- roc(outcome ~ s100b + ndka + wfns, data = aSAH)
g.list <- ggroc(roc.list)
g.list

# You can change the aesthetics as you normally would with ggplot2:
g.list + scale_colour_brewer(palette="RdGy")
g.list + scale_colour_manual(values = c("red", "blue", "black"))

# with additional aesthetics:
g3 <- ggroc(roc.list, linetype=2)
g3
g4 <- ggroc(roc.list, aes="linetype", color="red")
g4
# changing multiple aesthetics:
g5 <- ggroc(roc.list, aes=c("linetype", "color"))
g5

# OR faceting
g.list + facet_grid(.~name) + theme(legend.position="none")
}