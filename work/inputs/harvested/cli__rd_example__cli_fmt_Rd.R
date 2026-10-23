# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: cli_fmt.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 5

suppressPackageStartupMessages(library(cli))
cli_fmt({
  cli_alert_info("Loading data file")
  cli_alert_success("Loaded data file")
})