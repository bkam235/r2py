# r2py crawler metadata
# package: gert
# source_type: rd_example
# topic: git_signature.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\help
# lines: 13

suppressPackageStartupMessages(library(gert))
# Your default user
try(git_signature_default())

# Specify explicit name and email
git_signature("Some committer", "sarah@gmail.com")

# Create signature for an hour ago
(sig <- git_signature("Han", "han@company.com", Sys.time() - 3600))

# Parse a signature
git_signature_parse(sig)
git_signature_parse("Emma <emma@mu.edu>")