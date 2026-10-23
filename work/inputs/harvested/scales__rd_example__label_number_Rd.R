# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_number.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 48

suppressPackageStartupMessages(library(scales))
if (getRversion() >= "3.5") (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
demo_continuous(c(-1e6, 1e6))
demo_continuous(c(-1e6, 1e6), labels = label_number())
demo_continuous(c(-1e6, 1e6), labels = label_comma())

# Use scale to rescale very small or large numbers to generate
# more readable labels
demo_continuous(c(0, 1e6), labels = label_number())
demo_continuous(c(0, 1e6), labels = label_number(scale = 1 / 1e3))
demo_continuous(c(0, 1e-6), labels = label_number())
demo_continuous(c(0, 1e-6), labels = label_number(scale = 1e6))

#' Use scale_cut to automatically add prefixes for large/small numbers
demo_log10(
  c(1, 1e9),
  breaks = log_breaks(10),
  labels = label_number(scale_cut = cut_short_scale())
)
demo_log10(
  c(1, 1e9),
  breaks = log_breaks(10),
  labels = label_number(scale_cut = cut_si("m"))
)
demo_log10(
  c(1e-9, 1),
  breaks = log_breaks(10),
  labels = label_number(scale_cut = cut_si("g"))
)
# use scale and scale_cut when data already uses SI prefix
# for example, if data was stored in kg
demo_log10(
  c(1e-9, 1),
  breaks = log_breaks(10),
  labels = label_number(scale_cut = cut_si("g"), scale = 1e3)
)

#' # Use style arguments to vary the appearance of positive and negative numbers
demo_continuous(c(-1e3, 1e3), labels = label_number(
  style_positive = "plus",
  style_negative = "minus"
))
demo_continuous(c(-1e3, 1e3), labels = label_number(style_negative = "parens"))

# You can use prefix and suffix for other types of display
demo_continuous(c(32, 212), labels = label_number(suffix = "\u00b0F"))
demo_continuous(c(0, 100), labels = label_number(suffix = "\u00b0C"))
}) # examplesIf