# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: rectangle.window.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 4

suppressPackageStartupMessages(library(e1071))
x<-rnorm(500)
y<-stft(x, wtype="rectangle.window")
plot(y)