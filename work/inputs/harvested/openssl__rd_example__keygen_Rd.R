# r2py crawler metadata
# package: openssl
# source_type: rd_example
# topic: keygen.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\help
# lines: 9

suppressPackageStartupMessages(library(openssl))
# Generate keypair
key <- rsa_keygen()
pubkey <- as.list(key)$pubkey

# Write/read the key with a passphrase
write_pem(key, "id_rsa", password = "supersecret")
read_key("id_rsa", password = "supersecret")
unlink("id_rsa")