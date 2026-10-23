# r2py crawler metadata
# package: httpuv
# source_type: rd_example
# topic: ipFamily.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httpuv\help
# lines: 8

suppressPackageStartupMessages(library(httpuv))
ipFamily("127.0.0.1")   # 4
ipFamily("500.0.0.500") # -1
ipFamily("500.0.0.500") # -1

ipFamily("::")          # 6
ipFamily("::1")         # 6
ipFamily("fe80::1ff:fe23:4567:890a") # 6