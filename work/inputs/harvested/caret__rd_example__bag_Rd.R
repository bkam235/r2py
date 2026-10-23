# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: bag.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 28

suppressPackageStartupMessages(library(caret))
## A simple example of bagging conditional inference regression trees:
data(BloodBrain)

## treebag <- bag(bbbDescr, logBBB, B = 10,
##                bagControl = bagControl(fit = ctreeBag$fit,
##                                        predict = ctreeBag$pred,
##                                        aggregate = ctreeBag$aggregate))




## An example of pooling posterior probabilities to generate class predictions
data(mdrr)

## remove some zero variance predictors and linear dependencies
mdrrDescr <- mdrrDescr[, -nearZeroVar(mdrrDescr)]
mdrrDescr <- mdrrDescr[, -findCorrelation(cor(mdrrDescr), .95)]

## basicLDA <- train(mdrrDescr, mdrrClass, "lda")

## bagLDA2 <- train(mdrrDescr, mdrrClass,
##                  "bag",
##                  B = 10,
##                  bagControl = bagControl(fit = ldaBag$fit,
##                                          predict = ldaBag$pred,
##                                          aggregate = ldaBag$aggregate),
##                  tuneGrid = data.frame(vars = c((1:10)*10 , ncol(mdrrDescr))))