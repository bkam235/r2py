# r2py crawler metadata
# package: reprex
# source_type: rd_example
# topic: reprex_locale.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\reprex\help
# lines: 43

suppressPackageStartupMessages(library(reprex))
# if all you want to do is make sure messages are in English
reprex_locale("a" / 2)

# change messages to a specific language
reprex_locale(
  {
    "a" / 2
  },
  language = "it"
)

reprex_locale(
  {
    "a" / 2
  },
  language = "fr_CA"
)

reprex_locale(
  {
    "a" / 2
  },
  language = "pt_BR"
)

# get day-of-week and month to print in French (not Windows)
reprex_locale(
  {
    format(as.Date(c("2019-01-01", "2019-02-01")), "%a %b %d")
  },
  locale = c(LC_TIME = "fr_FR")
)

# get day-of-week and month to print in French (Windows)
# assumes that the relevant language is installed on the system
# LC_TIME can also be specified as "French" or "French_France" here
reprex_locale(
  {
    format(as.Date(c("2019-01-01", "2019-02-01")), "%a %b %d")
  },
  locale = c(LC_TIME = "French_France.1252")
)