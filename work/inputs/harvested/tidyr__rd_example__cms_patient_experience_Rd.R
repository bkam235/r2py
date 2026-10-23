# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: cms_patient_experience.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 28

suppressPackageStartupMessages(library(tidyr))
cms_patient_experience |>
  dplyr::distinct(measure_cd, measure_title)

cms_patient_experience |>
  pivot_wider(
    id_cols = starts_with("org"),
    names_from = measure_cd,
    values_from = prf_rate
 )

cms_patient_care |>
  pivot_wider(
    names_from = type,
    values_from = score
  )

cms_patient_care |>
  pivot_wider(
    names_from = measure_abbr,
    values_from = score
  )

cms_patient_care |>
  pivot_wider(
    names_from = c(measure_abbr, type),
    values_from = score
  )