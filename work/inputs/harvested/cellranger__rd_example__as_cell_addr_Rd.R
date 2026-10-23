# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: as.cell_addr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 16

suppressPackageStartupMessages(library(cellranger))
as.cell_addr(ra_ref())
rar <- ra_ref(2, TRUE, 5, TRUE)
as.cell_addr(rar)
## mixed reference
rar <- ra_ref(2, FALSE, 5, TRUE)
as.cell_addr(rar)
ra_ref_list <-
  list(ra_ref(), ra_ref(2, TRUE, 5, TRUE), ra_ref(2, FALSE, 5, TRUE))
as.cell_addr_v(ra_ref_list)
as.cell_addr("$D$12")
as.cell_addr("R4C3")
as.cell_addr(c("$C$4", "$D$12"))
as.cell_addr("$F2")
as.cell_addr("R[-4]C3")
as.cell_addr("F2", strict = FALSE)