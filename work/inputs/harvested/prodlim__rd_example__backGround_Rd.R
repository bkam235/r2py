# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: backGround.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 7

suppressPackageStartupMessages(library(prodlim))
plot(0,0)
backGround(bg="beige",fg="red",vertical=0,horizontal=0)

plot(0,0)
backGround(bg=c("yellow","green"),fg="red",xlim=c(-1,1),ylim=c(-1,1),horizontal=seq(0,1,.1))
backGround(bg=c("yellow","green"),fg="red",horizontal=seq(0,1,.1))