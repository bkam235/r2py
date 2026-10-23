# r2py crawler metadata
# package: gargle
# source_type: rd_example
# topic: cred_funs.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\help
# lines: 44

suppressPackageStartupMessages(library(gargle))
names(cred_funs_list())

creds_one <- function(scopes, ...) {}

cred_funs_add(one = creds_one)
cred_funs_add(two = creds_one, three = creds_one)
names(cred_funs_list())

cred_funs_add(two = NULL)
names(cred_funs_list())

# restore the default list
cred_funs_set_default()

# remove one specific credential fetcher
cred_funs_add(credentials_gce = NULL)
names(cred_funs_list())

# force the use of one specific credential fetcher
cred_funs_set(list(credentials_user_oauth2 = credentials_user_oauth2))
names(cred_funs_list())

# restore the default list
cred_funs_set_default()

# run some code with a temporary change to the registry
# creds_one ONLY
with_cred_funs(
  list(one = creds_one),
  names(cred_funs_list())
)
# add creds_one to the list
with_cred_funs(
  list(one = creds_one),
  names(cred_funs_list()),
  action = "modify"
)
# remove credentials_gce
with_cred_funs(
  list(credentials_gce = NULL),
  names(cred_funs_list()),
  action = "modify"
)