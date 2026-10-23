# r2py crawler metadata
# package: rprojroot
# source_type: vignette
# topic: rprojroot_s25
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rprojroot\doc\rprojroot.R
# lines: 9

suppressPackageStartupMessages(library(rprojroot))
try({
# Use the has_license criterion to find the root
R <- has_license$find_file
R

# Our package does not have a LICENSE file, trying to find the root results in an error
R()
})