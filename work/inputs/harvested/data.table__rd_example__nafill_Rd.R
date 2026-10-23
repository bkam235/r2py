# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: nafill.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 18

suppressPackageStartupMessages(library(data.table))
x = 1:10
x[c(1:2, 5:6, 9:10)] = NA
nafill(x, "locf")

x = c(1, NA, NaN, 3, NaN, NA, 4)
nafill(x, "locf")
nafill(x, "locf", nan=NaN)

# fill= applies to any leftover NA
nafill(c(NA, x), "locf")
nafill(c(NA, x), "locf", fill=0)

dt = data.table(v1=x, v2=shift(x)/2, v3=shift(x, -1L)/2)
nafill(dt, "nocb")

setnafill(dt, "locf", cols=c("v2","v3"))
dt