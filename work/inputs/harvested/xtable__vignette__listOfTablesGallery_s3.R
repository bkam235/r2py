# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: listOfTablesGallery_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\listOfTablesGallery.R
# lines: 14

require(xtable)
data(mtcars)
mtcars <- mtcars[, 1:6]
mtcarsList <- split(mtcars, f = mtcars$cyl)
### Reduce the size of the list elements
mtcarsList[[1]] <- mtcarsList[[1]][1,]
mtcarsList[[2]] <- mtcarsList[[2]][1:2,]
mtcarsList[[3]] <- mtcarsList[[3]][1:3,]
attr(mtcarsList, "subheadings") <- paste0("Number of cylinders = ",
                                          names(mtcarsList))
attr(mtcarsList, "message") <- c("Line 1 of Message",
                                 "Line 2 of Message")
str(mtcarsList)
attributes(mtcarsList)