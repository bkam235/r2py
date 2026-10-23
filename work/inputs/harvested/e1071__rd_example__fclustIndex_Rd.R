# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: fclustIndex.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 7

suppressPackageStartupMessages(library(e1071))
# a 2-dimensional example
x<-rbind(matrix(rnorm(100,sd=0.3),ncol=2),
         matrix(rnorm(100,mean=1,sd=0.3),ncol=2))
cl<-cmeans(x,2,20,verbose=TRUE,method="cmeans")
resultindexes <- fclustIndex(cl,x, index="all")
resultindexes