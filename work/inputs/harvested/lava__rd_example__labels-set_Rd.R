# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: labels-set.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 27

suppressPackageStartupMessages(library(lava))
m <- lvm(c(y,v)~x+z)
regression(m) <- c(v,x)~z
labels(m) <- c(y=expression(psi), z=expression(zeta))
nodecolor(m,~y+z+x,border=c("white","white","black"),
          labcol="white", lwd=c(1,1,5),
          lty=c(1,2)) <-  c("orange","indianred","lightgreen")
edgelabels(m,y~z+x, cex=c(2,1.5), col=c("orange","black"),labcol="darkblue",
           arrowhead=c("tee","dot"),
           lwd=c(3,1)) <- expression(phi,rho)
edgelabels(m,c(v,x)~z, labcol="red", cex=0.8,arrowhead="none") <- 2
if (interactive()) {
    plot(m,addstyle=FALSE)
}

m <- lvm(y~x)
labels(m) <- list(x="multiple\nlines")
if (interactive()) {
op <- par(mfrow=c(1,2))
plot(m,plain=TRUE)
plot(m)
par(op)

d <- sim(m,100)
e <- estimate(m,d)
plot(e,type="sd")
}