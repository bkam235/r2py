# r2py crawler metadata
# package: curl
# source_type: rd_example
# topic: nslookup.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\help
# lines: 6

suppressPackageStartupMessages(library(curl))
# Should always work if we are online
nslookup("www.r-project.org")

# If your OS supports IPv6
nslookup("ipv6.test-ipv6.com", ipv4_only = FALSE, error = FALSE)