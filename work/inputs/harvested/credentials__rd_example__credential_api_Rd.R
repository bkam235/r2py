# r2py crawler metadata
# package: credentials
# source_type: rd_example
# topic: credential_api.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\credentials\help
# lines: 12

suppressPackageStartupMessages(library(credentials))
# Insert example cred
example <- list(protocol = "https", host = "example.org",
  username = "test", password = "secret")
credential_approve(example)

# Retrieve it from the store
cred <- credential_fill(list(protocol = "https", host = "example.org", path = "/foo"))
print(cred)

# Delete it
credential_reject(cred)