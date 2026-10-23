# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: scheffe.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 13

suppressPackageStartupMessages(library(lava))
x <- rnorm(100)
d <- data.frame(y=rnorm(length(x),x),x=x)
l <- lm(y~x,d)
plot(y~x,d)
abline(l)
d0 <- data.frame(x=seq(-5,5,length.out=100))
d1 <- cbind(d0,predict(l,newdata=d0,interval="confidence"))
d2 <- cbind(d0,scheffe(l,d0))
lines(lwr~x,d1,lty=2,col="red")
lines(upr~x,d1,lty=2,col="red")
lines(lwr~x,d2,lty=2,col="blue")
lines(upr~x,d2,lty=2,col="blue")