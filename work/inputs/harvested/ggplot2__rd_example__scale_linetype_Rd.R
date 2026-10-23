# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: scale_linetype.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 19

suppressPackageStartupMessages(library(ggplot2))
base <- ggplot(economics_long, aes(date, value01))
base + geom_line(aes(group = variable))
base + geom_line(aes(linetype = variable))

# See scale_manual for more flexibility

# Common line types ----------------------------
df_lines <- data.frame(
  linetype = factor(
    1:4,
    labels = c("solid", "longdash", "dashed", "dotted")
  )
)
ggplot(df_lines) +
  geom_hline(aes(linetype = linetype, yintercept = 0), linewidth = 2) +
  scale_linetype_identity() +
  facet_grid(linetype ~ .) +
  theme_void(20)