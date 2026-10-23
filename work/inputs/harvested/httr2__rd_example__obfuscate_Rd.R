# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: obfuscate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 7

suppressPackageStartupMessages(library(httr2))
obfuscate("good morning")

# Every time you obfuscate you'll get a different value because it
# includes 16 bytes of random data which protects against certain types of
# brute force attack
obfuscate("good morning")