# r2py crawler metadata
# package: openssl
# source_type: rd_example
# topic: ec_dh.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\openssl\help
# lines: 12

suppressPackageStartupMessages(library(openssl))
# Need two EC keypairs from the same curve
alice_key <- ec_keygen("P-521")
bob_key <- ec_keygen("P-521")

# Derive public keys
alice_pub <- as.list(alice_key)$pubkey
bob_pub <- as.list(bob_key)$pubkey

# Both peers can derive the (same) shared secret via each other's pubkey
ec_dh(alice_key, bob_pub)
ec_dh(bob_key, alice_pub)