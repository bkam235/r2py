# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: num.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 60

suppressPackageStartupMessages(library(tibble))
# Display as a vector
num(9:11 * 100 + 0.5)

# Significant figures
tibble(
  x3 = num(9:11 * 100 + 0.5, sigfig = 3),
  x4 = num(9:11 * 100 + 0.5, sigfig = 4),
  x5 = num(9:11 * 100 + 0.5, sigfig = 5),
)

# Maximum digits after the decimal points
tibble(
  x0 = num(9:11 * 100 + 0.5, digits = 0),
  x1 = num(9:11 * 100 + 0.5, digits = -1),
  x2 = num(9:11 * 100 + 0.5, digits = -2),
)

# Use fixed digits and a currency label
tibble(
  usd = num(9:11 * 100 + 0.5, digits = 2, label = "USD"),
  gbp = num(9:11 * 100 + 0.5, digits = 2, label = "Â£"),
  chf = num(9:11 * 100 + 0.5, digits = 2, label = "SFr")
)

# Scale
tibble(
  small  = num(9:11 / 1000 + 0.00005, label = "%", scale = 100),
  medium = num(9:11 / 100 + 0.0005, label = "%", scale = 100),
  large  = num(9:11 / 10 + 0.005, label = "%", scale = 100)
)

# Notation
tibble(
  sci = num(10^(-13:6), notation = "sci"),
  eng = num(10^(-13:6), notation = "eng"),
  si  = num(10^(-13:6), notation = "si"),
  dec = num(10^(-13:6), notation = "dec")
)

# Fixed exponent
tibble(
  scimin = num(10^(-7:6) * 123, notation = "sci", fixed_exponent = -Inf),
  engmin = num(10^(-7:6) * 123, notation = "eng", fixed_exponent = -Inf),
  simin  = num(10^(-7:6) * 123, notation = "si", fixed_exponent = -Inf)
)

tibble(
  scismall = num(10^(-7:6) * 123, notation = "sci", fixed_exponent = -3),
  scilarge = num(10^(-7:6) * 123, notation = "sci", fixed_exponent = 3),
  scimax   = num(10^(-7:6) * 123, notation = "sci", fixed_exponent = Inf)
)

#' Extra significant digits
tibble(
  default = num(100 + 1:3 * 0.001),
  extra1 = num(100 + 1:3 * 0.001, extra_sigfig = TRUE),
  extra2 = num(100 + 1:3 * 0.0001, extra_sigfig = TRUE),
  extra3 = num(10000 + 1:3 * 0.00001, extra_sigfig = TRUE)
)