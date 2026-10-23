# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: hanning.window.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 6

suppressPackageStartupMessages(library(e1071))
hanning.window(10)

x<-rnorm(500)
y<-stft(x, wtype="hanning.window")
plot(y)