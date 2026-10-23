# r2py crawler metadata
# package: gtable
# source_type: rd_example
# topic: gtable_add_padding.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gtable\help
# lines: 13

suppressPackageStartupMessages(library(gtable))
library(grid)
gt <- gtable(unit(1, "null"), unit(1, "null"))
gt <- gtable_add_grob(gt, rectGrob(gp = gpar(fill = "black")), 1, 1)

plot(gt)
plot(cbind(gt, gt))
plot(rbind(gt, gt))

pad <- gtable_add_padding(gt, unit(1, "cm"))
plot(pad)
plot(cbind(pad, pad))
plot(rbind(pad, pad))