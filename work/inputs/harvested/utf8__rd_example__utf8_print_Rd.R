# r2py crawler metadata
# package: utf8
# source_type: rd_example
# topic: utf8_print.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\utf8\help
# lines: 16

suppressPackageStartupMessages(library(utf8))
# printing (assumes that output is capable of displaying Unicode 10.0.0)
print(intToUtf8(0x1F600 + 0:79)) # with default R print function
utf8_print(intToUtf8(0x1F600 + 0:79)) # with utf8_print, truncates line
utf8_print(intToUtf8(0x1F600 + 0:79), chars = 1000) # higher character limit

# in C locale, output ASCII (same results on all platforms)
oldlocale <- Sys.getlocale("LC_CTYPE")
invisible(Sys.setlocale("LC_CTYPE", "C")) # switch to C locale
utf8_print(intToUtf8(0x1F600 + 0:79))
invisible(Sys.setlocale("LC_CTYPE", oldlocale)) # switch back to old locale

# Mac and Linux only: style the names
# see https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
utf8_print(matrix(as.character(1:20), 4, 5),
           names = "1;4", rownames = "2;3")