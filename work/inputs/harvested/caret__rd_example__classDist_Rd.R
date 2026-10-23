# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: classDist.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 10

suppressPackageStartupMessages(library(caret))
trainSet <- sample(1:150, 100)

distData <- classDist(iris[trainSet, 1:4],
                      iris$Species[trainSet])

newDist <- predict(distData,
                   iris[-trainSet, 1:4])

splom(newDist, groups = iris$Species[-trainSet])