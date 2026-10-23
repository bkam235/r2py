# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: measure.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 38

suppressPackageStartupMessages(library(data.table))
(two.iris = data.table(datasets::iris)[c(1,150)])
# melt into a single value column.
melt(two.iris, measure.vars = measure(part, dim, sep="."))
# do the same, programmatically with measurev
my.list = list(part=NULL, dim=NULL)
melt(two.iris, measure.vars=measurev(my.list, sep="."))
# melt into two value columns, one for each part.
melt(two.iris, measure.vars = measure(value.name, dim, sep="."))
# melt into two value columns, one for each dim.
melt(two.iris, measure.vars = measure(part, value.name, sep="."))
# melt using sep, converting child number to integer.
(two.families = data.table(sex_child1="M", sex_child2="F", age_child1=10, age_child2=20))
print(melt(two.families, measure.vars = measure(
  value.name, child=as.integer,
  sep="_child"
)), class=TRUE)
# same melt using pattern.
print(melt(two.families, measure.vars = measure(
  value.name, child=as.integer,
  pattern="(.*)_child(.)"
)), class=TRUE)
# same melt with pattern and measurev function list.
print(melt(two.families, measure.vars = measurev(
  list(value.name=NULL, child=as.integer),
  pattern="(.*)_child(.)"
)), class=TRUE)
# inspired by data(who, package="tidyr")
(who <- data.table(id=1, new_sp_m5564=2, newrel_f65=3))
# melt to three variable columns, all character.
melt(who, measure.vars = measure(diagnosis, gender, ages, pattern="new_?(.*)_(.)(.*)"))
# melt to five variable columns, two numeric (with custom conversion).
print(melt(who, measure.vars = measure(
  diagnosis, gender, ages,
  ymin=as.numeric,
  ymax=function(y)ifelse(nzchar(y), as.numeric(y), Inf),
  pattern="new_?(.*)_(.)(([0-9]{2})([0-9]{0,2}))"
)), class=TRUE)