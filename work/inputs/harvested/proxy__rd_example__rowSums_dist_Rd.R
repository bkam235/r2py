# r2py crawler metadata
# package: proxy
# source_type: rd_example
# topic: rowSums.dist.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\proxy\help
# lines: 14

suppressPackageStartupMessages(library(proxy))
## 
x <- matrix(runif(10*2),ncol=2)
d <- dist(x)
rowSums(as.matrix(d))
rowSums.dist(d)			# the same

rowMeans(as.matrix(d))
rowMeans.dist(d)		# the same
rowMeans.dist(d, diag = FALSE)	# not the same
## NAs
d[3] <- NA
rowSums.dist(d, na.rm = TRUE)
rowMeans.dist(d, na.rm = TRUE)