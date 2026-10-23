# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: is_low_change.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 12

suppressPackageStartupMessages(library(knitr))
pdf(NULL)
dev.control("enable")  # enable plot recording
plot(1:10)
p1 = recordPlot()
abline(0, 1)  # add a line (a low-level change)
p2 = recordPlot()
plot(rnorm(100))
p3 = recordPlot()  # draw a completely new plot
dev.off()
knitr::is_low_change(p1, p2)  # true
knitr::is_low_change(p1, p3)  # false