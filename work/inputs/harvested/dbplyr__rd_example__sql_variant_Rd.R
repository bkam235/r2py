# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: sql_variant.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 27

suppressPackageStartupMessages(library(dbplyr))
# An example of adding some mappings for the statistical functions that
# postgresql provides: http://bit.ly/K5EdTn

postgres_agg <- sql_translator(.parent = base_agg,
  cor = sql_aggregate_2("CORR"),
  cov = sql_aggregate_2("COVAR_SAMP"),
  sd =  sql_aggregate("STDDEV_SAMP", "sd"),
  var = sql_aggregate("VAR_SAMP", "var")
)

# Next we have to simulate a connection that uses this variant
con <- simulate_dbi("TestCon")
sql_translation.TestCon <- function(x) {
  sql_variant(
    base_scalar,
    postgres_agg,
    base_no_win
  )
}

translate_sql(cor(x, y), con = con, window = FALSE)
translate_sql(sd(income / years), con = con, window = FALSE)

# Any functions not explicitly listed in the converter will be translated
# to sql as is, so you don't need to convert all functions.
translate_sql(regr_intercept(y, x), con = con)