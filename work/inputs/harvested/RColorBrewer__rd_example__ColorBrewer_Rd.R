# r2py crawler metadata
# package: RColorBrewer
# source_type: rd_example
# topic: ColorBrewer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\RColorBrewer\help
# lines: 31

suppressPackageStartupMessages(library(RColorBrewer))
## create a sequential palette for usage and show colors
mypalette<-brewer.pal(7,"Greens")
image(1:7,1,as.matrix(1:7),col=mypalette,xlab="Greens (sequential)",
       ylab="",xaxt="n",yaxt="n",bty="n")
## display a divergent palette
display.brewer.pal(7,"BrBG")
devAskNewPage(ask=TRUE)
## display a qualitative palette
display.brewer.pal(7,"Accent")
devAskNewPage(ask=TRUE)
## display a palettes simultanoeusly
display.brewer.all(n=10, exact.n=FALSE)
devAskNewPage(ask=TRUE)
display.brewer.all(n=10)
devAskNewPage(ask=TRUE)
display.brewer.all()
devAskNewPage(ask=TRUE)
display.brewer.all(type="div")
devAskNewPage(ask=TRUE)
display.brewer.all(type="seq")
devAskNewPage(ask=TRUE)
display.brewer.all(type="qual") 
devAskNewPage(ask=TRUE)
display.brewer.all(n=5,type="div",exact.n=TRUE)
devAskNewPage(ask=TRUE)
display.brewer.all(colorblindFriendly=TRUE)
devAskNewPage(ask=TRUE)
brewer.pal.info
brewer.pal.info["Blues",]
brewer.pal.info["Blues",]$maxcolors