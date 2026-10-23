# r2py crawler metadata
# package: openssl
# source_type: rd_example
# topic: my_key.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\help
# lines: 10

suppressPackageStartupMessages(library(openssl))
# Set random RSA key as default
key <- rsa_keygen()
write_pem(key, tmp <- tempfile(), password = "")
rm(key)
Sys.setenv("USER_KEY" = tmp)

# Check the new keys
print(my_key())
print(my_pubkey())