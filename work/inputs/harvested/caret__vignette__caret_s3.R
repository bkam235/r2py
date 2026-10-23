# r2py crawler metadata
# package: caret
# source_type: vignette
# topic: caret_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\doc\caret.R
# lines: 18

library(caret)
library(mlbench)
data(Sonar)

set.seed(107)
inTrain <- createDataPartition(
  y = Sonar$Class,
  ## the outcome data are needed
  p = .75,
  ## The percentage of data in the
  ## training set
  list = FALSE
)
## The format of the results

## The output is a set of integers for the rows of Sonar
## that belong in the training set.
str(inTrain)