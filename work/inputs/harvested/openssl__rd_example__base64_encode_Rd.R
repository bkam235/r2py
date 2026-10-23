# r2py crawler metadata
# package: openssl
# source_type: rd_example
# topic: base64_encode.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\help
# lines: 5

suppressPackageStartupMessages(library(openssl))
input <- charToRaw("foo = bar + 5")
message <- base64_encode(input)
output <- base64_decode(message)
identical(output, input)