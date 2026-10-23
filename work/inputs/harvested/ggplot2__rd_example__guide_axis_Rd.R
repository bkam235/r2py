# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: guide_axis.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 13

suppressPackageStartupMessages(library(ggplot2))
# plot with overlapping text
p <- ggplot(mpg, aes(cty * 100, hwy * 100)) +
  geom_point() +
  facet_wrap(vars(class))

# axis guides can be customized in the scale_* functions or
# using guides()
p + scale_x_continuous(guide = guide_axis(n.dodge = 2))
p + guides(x = guide_axis(angle = 90))

# can also be used to add a duplicate guide
p + guides(x = guide_axis(n.dodge = 2), y.sec = guide_axis())