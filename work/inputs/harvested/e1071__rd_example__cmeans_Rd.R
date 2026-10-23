# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: cmeans.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 13

suppressPackageStartupMessages(library(e1071))
# a 2-dimensional example
x<-rbind(matrix(rnorm(100,sd=0.3),ncol=2),
         matrix(rnorm(100,mean=1,sd=0.3),ncol=2))
cl<-cmeans(x,2,20,verbose=TRUE,method="cmeans",m=2)
print(cl)

# a 3-dimensional example
x<-rbind(matrix(rnorm(150,sd=0.3),ncol=3),
         matrix(rnorm(150,mean=1,sd=0.3),ncol=3),
         matrix(rnorm(150,mean=2,sd=0.3),ncol=3))
cl<-cmeans(x,6,20,verbose=TRUE,method="cmeans")
print(cl)