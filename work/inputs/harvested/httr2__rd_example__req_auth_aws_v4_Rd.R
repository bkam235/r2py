# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_auth_aws_v4.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 22

suppressPackageStartupMessages(library(httr2))
if (httr2:::has_paws_credentials()) withAutoprint({ # examplesIf
creds <- paws.common::locate_credentials()
model_id <- "anthropic.claude-3-5-sonnet-20240620-v1:0"
req <- request("https://bedrock-runtime.us-east-1.amazonaws.com")
# https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html
req <- req_url_path_append(req, "model", model_id, "converse")
req <- req_body_json(req, list(
  messages = list(list(
    role = "user",
    content = list(list(text = "What's your name?"))
  ))
))
req <- req_auth_aws_v4(
  req,
  aws_access_key_id = creds$access_key_id,
  aws_secret_access_key = creds$secret_access_key,
  aws_session_token = creds$session_token
)
resp <- req_perform_connection(req)
str(resp_body_json(resp))
}) # examplesIf