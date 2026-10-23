# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: SmartControl.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 16

suppressPackageStartupMessages(library(prodlim))
myPlot = function(...){
 ## set defaults
 plot.DefaultArgs=list(x=0,y=0,type="n")
 lines.DefaultArgs=list(x=1:10,lwd=3)
 ## apply smartcontrol
 x=SmartControl(call=list(...),
           defaults=list("plot"=plot.DefaultArgs, "lines"=lines.DefaultArgs),
        ignore.case=TRUE,keys=c("plot","axis2","lines"),
             forced=list("plot"=list(axes=FALSE),"axis2"=list(side=2)))
 ## call subroutines
 do.call("plot",x$plot)
 do.call("lines",x$lines)
 do.call("axis",x$axis2)
}
myPlot(plot.ylim=c(0,5),plot.xlim=c(0,20),lines.lty=3,axis2.At=c(0,3,4))