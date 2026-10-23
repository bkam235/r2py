# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: pal_dichromat.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 9

suppressPackageStartupMessages(library(scales))
if (requireNamespace("dichromat", quietly = TRUE)) {
  show_col(pal_dichromat("BluetoOrange.10")(10))
  show_col(pal_dichromat("BluetoOrange.10")(5))

  # Can use with gradient_n to create a continuous gradient
  cols <- pal_dichromat("DarkRedtoBlue.12")(12)
  show_col(pal_gradient_n(cols)(seq(0, 1, length.out = 30)))
}