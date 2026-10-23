# r2py crawler metadata
# package: ipred
# source_type: rd_example
# topic: predict.inbagg.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ipred\help
# lines: 15

suppressPackageStartupMessages(library(ipred))
library("MASS")
library("rpart")
y <- as.factor(sample(1:2, 100, replace = TRUE))
W <- mvrnorm(n = 200, mu = rep(0, 3), Sigma = diag(3)) 
X <- mvrnorm(n = 200, mu = rep(2, 3), Sigma = diag(3))
colnames(W) <- c("w1", "w2", "w3")
colnames(X) <- c("x1", "x2", "x3")
DATA <- data.frame(y, W, X)

pFUN <- list(list(formula = w1~x1+x2, model = lm),
list(model = rpart))

RES <- inbagg(y~w1+w2+w3~x1+x2+x3, data = DATA, pFUN = pFUN)
predict(RES, newdata = X)