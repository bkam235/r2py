# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: update_blueprint.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 13

suppressPackageStartupMessages(library(hardhat))
blueprint <- default_xy_blueprint()

# `intercept` defaults to FALSE
blueprint

update_blueprint(blueprint, intercept = TRUE)

# Can't update non-existent elements
try(update_blueprint(blueprint, intercpt = TRUE))

# Can't add non-valid elements
try(update_blueprint(blueprint, intercept = 1))