# r2py crawler metadata
# package: openssl
# source_type: rd_example
# topic: encrypt_envelope.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\help
# lines: 13

suppressPackageStartupMessages(library(openssl))
# Requires RSA key
key <- rsa_keygen()
pubkey <- key$pubkey
msg <- serialize(iris, NULL)

# Encrypt
out <- encrypt_envelope(msg, pubkey)
str(out)

# Decrypt
orig <- decrypt_envelope(out$data, out$iv, out$session, key)
stopifnot(identical(msg, orig))