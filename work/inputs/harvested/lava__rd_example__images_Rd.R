# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: images.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 15

suppressPackageStartupMessages(library(lava))
X <- matrix(rbinom(400,3,0.5),20)
group <- rep(1:4,each=5)
images(X,colorbar=0,zlim=c(0,3))
images(X,group=group,zlim=c(0,3))

images(X,group=group,col=list(RColorBrewer::brewer.pal(4,"Purples"),
                               RColorBrewer::brewer.pal(4,"Greys"),
                               RColorBrewer::brewer.pal(4,"YlGn"),
                               RColorBrewer::brewer.pal(4,"PuBuGn")),colorbar=2,zlim=c(0,3))

images(list(X,X,X,X),group=group,zlim=c(0,3))
images(list(X,X,X,X),ncol=1,group=group,zlim=c(0,3))
images(list(X,X),group,axis2=c(FALSE,FALSE),axis1=c(FALSE,FALSE),
      mar=list(c(0,0,0,0),c(0,0,0,0)),yaxs="i",xaxs="i",zlim=c(0,3))