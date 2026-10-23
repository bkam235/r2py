# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: plot.tune.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 6

suppressPackageStartupMessages(library(e1071))
data(iris)
  obj <- tune.svm(Species~., data = iris, sampling = "fix",
                  gamma = 2^c(-8,-4,0,4), cost = 2^c(-8,-4,-2,0))
  plot(obj, transform.x = log2, transform.y = log2)
  plot(obj, type = "perspective", theta = 120, phi = 45)