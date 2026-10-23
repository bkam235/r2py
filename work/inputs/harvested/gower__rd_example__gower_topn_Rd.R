# r2py crawler metadata
# package: gower
# source_type: rd_example
# topic: gower_topn.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gower\help
# lines: 5

suppressPackageStartupMessages(library(gower))
# find the top 4 best matches in the iris data set with itself.
x <- iris[1:3,]
lookup <- iris[1:10,]
gower_topn(x=x,y=lookup,n=4)