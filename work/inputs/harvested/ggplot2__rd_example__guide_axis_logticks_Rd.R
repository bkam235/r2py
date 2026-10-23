# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: guide_axis_logticks.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 35

suppressPackageStartupMessages(library(ggplot2))
# A standard plot
p <- ggplot(msleep, aes(bodywt, brainwt)) +
  geom_point(na.rm = TRUE)

# The logticks axis works well with log scales
p + scale_x_log10(guide = "axis_logticks") +
  scale_y_log10(guide = "axis_logticks")

# Or with log-transformed coordinates
p + coord_transform(x = "log10", y = "log10") +
  guides(x = "axis_logticks", y = "axis_logticks")

# When data is transformed manually, one should provide `prescale.base`
# Keep in mind that this axis uses log10 space for placement, not log2
p + aes(x = log2(bodywt), y = log10(brainwt)) +
  guides(
    x = guide_axis_logticks(prescale.base = 2),
    y = guide_axis_logticks(prescale.base = 10)
  )

# A plot with both positive and negative extremes, pseudo-log transformed
set.seed(42)
p2 <- ggplot(data.frame(x = rcauchy(1000)), aes(x = x)) +
  geom_density() +
  scale_x_continuous(
    breaks = c(-10^(4:0), 0, 10^(0:4)),
    transform = "pseudo_log"
  )

# The log ticks are mirrored when 0 is included
p2 + guides(x = "axis_logticks")

# To control the tick density around 0, one can set `negative.small`
p2 + guides(x = guide_axis_logticks(negative.small = 1))