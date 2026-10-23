# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_relabel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 18

suppressPackageStartupMessages(library(forcats))
gss_cat$partyid |> fct_count()
gss_cat$partyid |>
  fct_relabel(\(x) gsub(",", ", ", x)) |>
  fct_count()

convert_income <- function(x) {
  regex <- "^(?:Lt |)[$]([0-9]+).*$"
  is_range <- grepl(regex, x)
  num_income <- as.numeric(gsub(regex, "\\1", x[is_range]))
  num_income <- trunc(num_income / 5000) * 5000
  x[is_range] <- paste0("Gt $", num_income)
  x
}
fct_count(gss_cat$rincome)
convert_income(levels(gss_cat$rincome))
rincome2 <- fct_relabel(gss_cat$rincome, convert_income)
fct_count(rincome2)