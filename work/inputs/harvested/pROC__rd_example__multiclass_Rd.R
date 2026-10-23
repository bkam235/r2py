# r2py crawler metadata
# package: pROC
# source_type: rd_example
# topic: multiclass.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pROC\help
# lines: 63

suppressPackageStartupMessages(library(pROC))
####
# Examples for a univariate decision value
####
data(aSAH)

# Basic example
multiclass.roc(aSAH$gos6, aSAH$s100b)
# Produces an innocuous warning because one level has no observation

# Select only 3 of the aSAH$gos6 levels:
multiclass.roc(aSAH$gos6, aSAH$s100b, levels=c(3, 4, 5))

# Give the result in percent
multiclass.roc(aSAH$gos6, aSAH$s100b, percent=TRUE)

####
# Examples for multivariate decision values (e.g. class probabilities)
####


# Example with a multinomial log-linear model from nnet
# We use the iris dataset and split into a training and test set
requireNamespace("nnet")
data(iris)
iris.sample <- sample(1:150)
iris.train <- iris[iris.sample[1:75],]
iris.test <- iris[iris.sample[76:150],]
mn.net <- nnet::multinom(Species ~ ., iris.train)

# Use predict with type="prob" to get class probabilities
iris.predictions <- predict(mn.net, newdata=iris.test, type="prob")
head(iris.predictions)

# This can be used directly in multiclass.roc:
multiclass.roc(iris.test$Species, iris.predictions)



# Let's see an other example with an artificial dataset
n <- c(100, 80, 150)
responses <- factor(c(rep("X1", n[1]), rep("X2", n[2]), rep("X3", n[3])))
# construct prediction matrix: one column per class

preds <- lapply(n, function(x) runif(x, 0.4, 0.6))
predictor <- as.matrix(data.frame(
                "X1" = c(preds[[1]], runif(n[2] + n[3], 0, 0.7)),
                "X2" = c(runif(n[1], 0.1, 0.4), preds[[2]], runif(n[3], 0.2, 0.8)),
                "X3" = c(runif(n[1] + n[2], 0.3, 0.7), preds[[3]])
             ))
multiclass.roc(responses, predictor)

# One can change direction , partial.auc, percent, etc:
multiclass.roc(responses, predictor, direction = ">")
multiclass.roc(responses, predictor, percent = TRUE, 
	partial.auc = c(100, 90), partial.auc.focus = "se")


# Limit set of levels
multiclass.roc(responses, predictor, levels = c("X1", "X2"))
# Use with formula. Here we need a data.frame to store the responses as characters
data <- cbind(as.data.frame(predictor), "response" = responses)
multiclass.roc(response ~ X1+X3, data)