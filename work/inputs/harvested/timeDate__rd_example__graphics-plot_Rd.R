# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: graphics-plot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 12

suppressPackageStartupMessages(library(timeDate))
## timeCalendar
x <- timeCalendar()
y <- rnorm(12)

## Plotting
plot(x, y, type = "l")
points(x, y, pch = 19, col = "red")

plot(x, y, type = "l", xaxt = "n")
axis.timeDate(1, at = x[c(1, 3, 5, 7, 9, 11)], format = "%b")
axis.timeDate(1, at = x[12], format = "%Y")