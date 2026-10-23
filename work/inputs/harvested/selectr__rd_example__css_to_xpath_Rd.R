# r2py crawler metadata
# package: selectr
# source_type: rd_example
# topic: css_to_xpath.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\selectr\help
# lines: 5

suppressPackageStartupMessages(library(selectr))
css_to_xpath(".testclass")
  css_to_xpath("#testid", prefix = "")
  css_to_xpath("#testid .testclass")
  css_to_xpath(":checked", translator = "html")