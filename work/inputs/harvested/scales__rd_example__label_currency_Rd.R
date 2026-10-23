# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_currency.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 35

suppressPackageStartupMessages(library(scales))
demo_continuous(c(0, 1), labels = label_currency())
demo_continuous(c(1, 100), labels = label_currency())

# Customise currency display with prefix and suffix
demo_continuous(c(1, 100), labels = label_currency(prefix = "USD "))
yen <- label_currency(
  prefix = "Â¥",
  suffix = "",
  big.mark = ".",
  decimal.mark = ","
)
demo_continuous(c(1000, 1100), labels = yen)

# Use style_negative = "parens" for finance style display
demo_continuous(c(-100, 100), labels = label_currency(style_negative = "parens"))

# Use scale_cut to use K/M/B where appropriate
demo_log10(c(1, 1e16),
  breaks = log_breaks(7, 1e3),
  labels = label_currency(scale_cut = cut_short_scale())
)
# cut_short_scale() uses B = one thousand million
# cut_long_scale() uses B = one million million
demo_log10(c(1, 1e16),
  breaks = log_breaks(7, 1e3),
  labels = label_currency(scale_cut = cut_long_scale())
)

# You can also define your own breaks
gbp <- label_currency(
  prefix = "\u00a3",
  scale_cut = c(0, k = 1e3, m = 1e6, bn = 1e9, tn = 1e12)
)
demo_log10(c(1, 1e12), breaks = log_breaks(5, 1e3), labels = gbp)