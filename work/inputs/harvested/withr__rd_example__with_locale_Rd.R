# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_locale.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 23

suppressPackageStartupMessages(library(withr))
## Change locale for time:
df <- data.frame(
  stringsAsFactors = FALSE,
  date = as.Date(c("2019-01-01", "2019-02-01")),
  value = c(1, 2)
)
with_locale(new = c("LC_TIME" = "es_ES"), code = plot(df$date, df$value))
## Compare with:
#  plot(df$date, df$value)

## Month names:
with_locale(new = c("LC_TIME" = "en_GB"), format(ISOdate(2000, 1:12, 1), "%B"))
with_locale(new = c("LC_TIME" = "es_ES"), format(ISOdate(2000, 1:12, 1), "%B"))

## Change locale for currencies:
with_locale(new = c("LC_MONETARY" = "it_IT"), Sys.localeconv())
with_locale(new = c("LC_MONETARY" = "en_US"), Sys.localeconv())

## Ordering:
x <- c("bernard", "bÃ©rÃ©nice", "bÃ©atrice", "boris")
with_locale(c(LC_COLLATE = "fr_FR"), sort(x))
with_locale(c(LC_COLLATE = "C"), sort(x))