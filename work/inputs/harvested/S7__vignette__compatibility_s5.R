# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: compatibility_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\compatibility.R
# lines: 8

suppressPackageStartupMessages(library(S7))
new_rle <- new_class("rle",
  parent = class_list,
  constructor = function(lengths, values) {
    new_object(list(lengths = lengths, values = values))
  }
)
rle(1:10)