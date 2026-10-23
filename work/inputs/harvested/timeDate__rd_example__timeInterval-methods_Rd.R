# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: timeInterval-methods.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 23

suppressPackageStartupMessages(library(timeDate))
timeInterval(left = "2024-12-20", right = "2024-12-21")
timeInterval(left = "2024-12-20 10:00", right = "2024-12-21 11:00")

timeInterval(left = c("2024-12-20 10:00", "2024-12-22 10:00"),
             right = c("2024-12-21 11:00", "2024-12-23 11:00"))

## overlapping or touching intervals are combined
timeInterval(left = c("2024-12-20 10:00", "2024-12-21 10:00"),
             right = c("2024-12-21 11:00", "2024-12-23 11:00"))
timeInterval(left = c("2024-12-20 10:00", "2024-12-21 08:00"),
             right = c("2024-12-21 11:00", "2024-12-23 11:00"))

## create timeInterval by rounding down and up  times inside the desired unit
timeInterval(as.Date("2024-12-20"))
timeInterval(timeDate("2024-12-20 10:20:30"), unit = "days")
timeInterval(right = timeDate("2024-12-20 10:20:30"), unit = "days")

timeInterval(timeDate("2024-12-20 10:20:30"), unit = "hours")
timeInterval(right = timeDate("2024-12-20 10:20:30"), unit = "hours")

timeInterval(timeDate("2024-12-20 10:20:30"), unit = "mins")
timeInterval(right = timeDate("2024-12-20 10:20:30"), unit = "mins")