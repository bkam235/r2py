# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: os.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 7

library(xfun)
# only one of the following statements should be true
is_windows()
is_unix() && is_macos()
is_linux()
# In newer Macs, CPU can be either Intel or Apple
is_arm64()  # TRUE on Apple silicone machines