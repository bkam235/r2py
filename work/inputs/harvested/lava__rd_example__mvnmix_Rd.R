# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: mvnmix.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 10

suppressPackageStartupMessages(library(lava))
data(faithful)
set.seed(1)
M1 <- mvnmix(faithful[,"waiting",drop=FALSE],k=2)
M2 <- mvnmix(faithful,k=2)
if (interactive()) {
    par(mfrow=c(2,1))
    plot(M1,col=c("orange","blue"),ylim=c(0,0.05))
    plot(M2,col=c("orange","blue"))
}