# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: maxindex.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 11

suppressPackageStartupMessages(library(bit))
r <- ri(1, 2, 12)
i <- as.which(r)
w <- as.bitwhich(r)
b <- as.bit(r)
l <- as.logical(r)
u <- which(l)      # unclassed which

sapply(list(r=r, u=u, i=i, w=w, b=b, l=l), function(x) {
  c(length=length(x), sum=sum(x), maxindex=maxindex(x), poslength=poslength(x))
})