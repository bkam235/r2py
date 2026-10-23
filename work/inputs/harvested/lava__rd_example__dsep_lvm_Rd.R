# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: dsep.lvm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 8

suppressPackageStartupMessages(library(lava))
m <- lvm(x5 ~ x4+x3, x4~x3+x1, x3~x2, x2~x1)
if (interactive()) {
plot(m,layoutType='neato')
}
dsep(m,x5~x1|x2+x4)
dsep(m,x5~x1|x3+x4)
dsep(m,~x1+x2+x3|x4)