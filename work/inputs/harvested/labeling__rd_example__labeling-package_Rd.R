# r2py crawler metadata
# package: labeling
# source_type: rd_example
# topic: labeling-package.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\labeling\help
# lines: 17

suppressPackageStartupMessages(library(labeling))
heckbert(8.1, 14.1, 4)	# 5 10 15
wilkinson(8.1, 14.1, 4)	# 8 9 10 11 12 13 14 15
extended(8.1, 14.1, 4)	# 8 10 12 14
# When plotting, extend the plot range to include the labeling
# Should probably have a helper function to make this easier
data(iris)
x <- iris$Sepal.Width
y <- iris$Sepal.Length
xl <- extended(min(x), max(x), 6)
yl <- extended(min(y), max(y), 6)
plot(x, y,
    xlim=c(min(x,xl),max(x,xl)),
    ylim=c(min(y,yl),max(y,yl)),
    axes=FALSE, main="Extended labeling")
axis(1, at=xl)
axis(2, at=yl)