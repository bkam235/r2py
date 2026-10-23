# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: print.data.table.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 69

suppressPackageStartupMessages(library(data.table))
#output compression
  DT <- data.table(a = 1:1000)
  print(DT, nrows = 100, topn = 4)

  #`quote` can be used to identify whitespace
  DT <- data.table(blanks = c(" 12", " 34"),
                   noblanks = c("12", "34"))
  print(DT, quote = TRUE)

  #`class` provides handy column type summaries at a glance
  DT <- data.table(a = vector("integer", 3),
                   b = vector("complex", 3),
                   c = as.IDate(paste0("2016-02-0", 1:3)))
  print(DT, class = TRUE)

  #`row.names` can be eliminated to save space
  DT <- data.table(a = 1:3)
  print(DT, row.names = FALSE)

  #`print.keys` can alert which columns are currently keys
  DT <- data.table(a=1:3, b=4:6, c=7:9, key=c("b", "a"))
  setindexv(DT, c("a", "b"))
  setindexv(DT, "a")
  print(DT, print.keys=TRUE)

  # `trunc.cols` will make it so only columns that fit in console will be printed
  #    with a message that states the variables not shown
  old_width = options("width" = 40)
  DT <- data.table(thing_11 = vector("integer", 3),
                   thing_21 = vector("complex", 3),
                   thing_31 = as.IDate(paste0("2016-02-0", 1:3)),
                   thing_41 = "aasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf",
                   thing_51 = vector("integer", 3),
                   thing_61 = vector("complex", 3))
  print(DT, trunc.cols=TRUE)
  options(old_width)

  # `char.trunc` will truncate the strings,
  # if their lengths exceed the given limit: `datatable.prettyprint.char`
  # For example:

  old = options(datatable.prettyprint.char=5L)
  DT = data.table(x=1:2, y=c("abcdefghij", "klmnopqrstuv"))
  DT
  options(old)

  # Formatting customization
  format_col.complex = function(x, ...) sprintf('(%.1f, %.1fi)', Re(x), Im(x))
  x = data.table(z = c(1 + 3i, 2 - 1i, pi + 2.718i))
  print(x)

  old = options(datatable.show.indices=TRUE)
  NN = 200
  set.seed(2024)
  DT = data.table(
    grp1 = sample(100, NN, TRUE),
    grp2 = sample(90, NN, TRUE),
    grp3 = sample(80, NN, TRUE)
  )
  setkey(DT, grp1, grp2)
  setindex(DT, grp1, grp3)
  print(DT)
  options(old)

  iris = as.data.table(iris)
  iris_agg = iris[ , .(reg = list(lm(Sepal.Length ~ Petal.Length))), by = Species]
  format_list_item.lm = function(x, ...) sprintf('<lm:%s>', format(x$call$formula))
  print(iris_agg)