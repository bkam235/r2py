# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: check_device.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 19

suppressPackageStartupMessages(library(ggplot2))
# Typically you'd run `check_device()` inside a function that might produce
# advanced graphics.
# The check is designed for use in control flow statements in the test mode
if (check_device("patterns", action = "test")) {
  print("Yay")
} else {
  print("Nay")
}

# Automatically throw a warning when unavailable
if (check_device("compositing", action = "warn")) {
  print("Yay")
} else {
  print("Nay")
}

# Possibly throw an error
try(check_device("glyphs", action = "abort"))