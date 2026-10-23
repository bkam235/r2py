# r2py crawler metadata
# package: bit64
# source_type: rd_example
# topic: optimizer64.data.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit64\help
# lines: 19

suppressPackageStartupMessages(library(bit64))
data(optimizer64.data)
print(optimizer64.data)
oldpar <- par(no.readonly = TRUE)
par(mfrow=c(2,1))
par(cex=0.7)
for (i in 1:nrow(optimizer64.data)){
 for (j in 1:2){
   tim <- optimizer64.data[[i,j]]
  barplot(t(tim))
  if (rownames(optimizer64.data)[i]=="match")
   title(paste("match", colnames(optimizer64.data)[j], "in", colnames(optimizer64.data)[3-j]))
  else if (rownames(optimizer64.data)[i]=="%in%")
   title(paste(colnames(optimizer64.data)[j], "%in%", colnames(optimizer64.data)[3-j]))
  else
   title(paste(rownames(optimizer64.data)[i], colnames(optimizer64.data)[j]))
 }
}
par(mfrow=c(1,1))