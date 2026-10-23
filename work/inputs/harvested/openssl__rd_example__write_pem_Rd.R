# r2py crawler metadata
# package: openssl
# source_type: rd_example
# topic: write_pem.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\help
# lines: 9

suppressPackageStartupMessages(library(openssl))
# Generate RSA keypair
key <- rsa_keygen()
pubkey <- key$pubkey

# Write to output formats
write_ssh(pubkey)
write_pem(pubkey)
write_pem(key, password = "super secret")