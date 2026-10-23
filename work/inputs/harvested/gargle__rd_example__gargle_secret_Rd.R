# r2py crawler metadata
# package: gargle
# source_type: rd_example
# topic: gargle_secret.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\help
# lines: 47

suppressPackageStartupMessages(library(gargle))
if (secret_has_key("GARGLE_KEY")) withAutoprint({ # examplesIf
# gargle ships with JSON for a fake service account
# here we put the encrypted JSON into a new file
tmp <- tempfile()
secret_encrypt_json(
  fs::path_package("gargle", "extdata", "fake_service_account.json"),
  tmp,
  key = "GARGLE_KEY"
)

# complete the round trip by providing the decrypted JSON to a credential
# function
credentials_service_account(
 scopes = "https://www.googleapis.com/auth/userinfo.email",
 path = secret_decrypt_json(
   fs::path_package("gargle", "secret", "gargle-testing.json"),
   key = "GARGLE_KEY"
 )
)

file.remove(tmp)

# make an artificial Gargle2.0 token
fauxen <- gargle2.0_token(
  email = "jane@example.org",
  client = gargle_oauth_client(
    id = "CLIENT_ID", secret = "SECRET", name = "CLIENT"
  ),
  credentials = list(token = "fauxen"),
  cache = FALSE
)
fauxen

# store the fake token in an encrypted file
tmp2 <- tempfile()
secret_write_rds(fauxen, path = tmp2, key = "GARGLE_KEY")

# complete the round trip by providing the decrypted token to the "BYO token"
# credential function
rt_fauxen <- credentials_byo_oauth2(
  token  = secret_read_rds(tmp2, key = "GARGLE_KEY")
)
rt_fauxen

file.remove(tmp2)
}) # examplesIf