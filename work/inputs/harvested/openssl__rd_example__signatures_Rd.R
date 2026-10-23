# r2py crawler metadata
# package: openssl
# source_type: rd_example
# topic: signatures.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\help
# lines: 31

suppressPackageStartupMessages(library(openssl))
# Generate a keypair
key <- rsa_keygen()
pubkey <- key$pubkey

# Sign a file
data <- system.file("DESCRIPTION")
sig <- signature_create(data, sha256, key = key)
stopifnot(signature_verify(data, sig, sha256, pubkey = pubkey))

# Sign raw data
data <- serialize(iris, NULL)
sig <- signature_create(data, sha256, key = key)
stopifnot(signature_verify(data, sig, sha256, pubkey = pubkey))

# Sign a hash
md <- md5(data)
sig <- signature_create(md, hash = sha256, key = key)
stopifnot(signature_verify(md, sig, hash = sha256, pubkey = pubkey))
#
# ECDSA example
data <- serialize(iris, NULL)
key <- ec_keygen()
pubkey <- key$pubkey
sig <- signature_create(data, sha256, key = key)
stopifnot(signature_verify(data, sig, sha256, pubkey = pubkey))

# Convert signature to (r, s) parameters and then back
params <- ecdsa_parse(sig)
out <- ecdsa_write(params$r, params$s)
identical(sig, out)