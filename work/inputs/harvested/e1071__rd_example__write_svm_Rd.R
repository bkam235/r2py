# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: write.svm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 22

suppressPackageStartupMessages(library(e1071))
data(iris)
attach(iris)

## classification mode
# default with factor response:
model <- svm (Species~., data=iris)

# export SVM object to (temporary) files
svm_file <- tempfile()
scale_file <- tempfile()

write.svm(model, svm.file = svm_file, scale.file = scale_file)

# read scale file
# the n-th row is corresponding to n-th dimension. The 1st column contains the
# center value, the 2nd column is the scale value.
read.table(scale_file)

# clean up
unlink(svm_file)
unlink(scale_file)