# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: tune.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 39

suppressPackageStartupMessages(library(e1071))
data(iris)
  ## tune `svm' for classification with RBF-kernel (default in svm),
  ## using one split for training/validation set
  
  obj <- tune(svm, Species~., data = iris, 
              ranges = list(gamma = 2^(-1:1), cost = 2^(2:4)),
              tunecontrol = tune.control(sampling = "fix")
             )

  ## alternatively:
  ## obj <- tune.svm(Species~., data = iris, gamma = 2^(-1:1), cost = 2^(2:4))

  summary(obj)
  plot(obj)

  ## tune `knn' using a convenience function; this time with the
  ## conventional interface and bootstrap sampling:
  x <- iris[,-5]
  y <- iris[,5]
  obj2 <- tune.knn(x, y, k = 1:5, tunecontrol = tune.control(sampling = "boot"))
  summary(obj2)
  plot(obj2)

  ## tune `gknn' using the formula interface.
  ## (Use Euclidean distances instead of Gower metric)
  obj3 <- tune.gknn(Species ~ ., data = iris, k = 1:5, method = "Euclidean")
  summary(obj3)
  plot(obj3)
  

  ## tune `rpart' for regression, using 10-fold cross validation (default)
  data(mtcars)
  obj4 <- tune.rpart(mpg~., data = mtcars, minsplit = c(5,10,15))
  summary(obj4)
  plot(obj4)

  ## simple error estimation for lm using 10-fold cross validation
  tune(lm, mpg~., data = mtcars)