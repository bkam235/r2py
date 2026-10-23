# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: densityplot.rfe.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 30

suppressPackageStartupMessages(library(caret))
library(mlbench)
n <- 100
p <- 40
sigma <- 1
set.seed(1)
sim <- mlbench.friedman1(n, sd = sigma)
x <- cbind(sim$x,  matrix(rnorm(n * p), nrow = n))
y <- sim$y
colnames(x) <- paste("var", 1:ncol(x), sep = "")

normalization <- preProcess(x)
x <- predict(normalization, x)
x <- as.data.frame(x, stringsAsFactors = TRUE)
subsets <- c(10, 15, 20, 25)

ctrl <- rfeControl(
                   functions = lmFuncs,
                   method = "cv",
                   verbose = FALSE,
                   returnResamp = "all")

lmProfile <- rfe(x, y,
                 sizes = subsets,
                 rfeControl = ctrl)
xyplot(lmProfile)
stripplot(lmProfile)

histogram(lmProfile)
densityplot(lmProfile)