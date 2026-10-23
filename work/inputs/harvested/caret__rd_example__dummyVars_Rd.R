# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: dummyVars.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 43

suppressPackageStartupMessages(library(caret))
when <- data.frame(time = c("afternoon", "night", "afternoon",
                            "morning", "morning", "morning",
                            "morning", "afternoon", "afternoon"),
                   day = c("Mon", "Mon", "Mon",
                           "Wed", "Wed", "Fri",
                           "Sat", "Sat", "Fri"),
                           stringsAsFactors = TRUE)

levels(when$time) <- list(morning="morning",
                          afternoon="afternoon",
                          night="night")
levels(when$day) <- list(Mon="Mon", Tue="Tue", Wed="Wed", Thu="Thu",
                         Fri="Fri", Sat="Sat", Sun="Sun")

## Default behavior:
model.matrix(~day, when)

mainEffects <- dummyVars(~ day + time, data = when)
mainEffects
predict(mainEffects, when[1:3,])

when2 <- when
when2[1, 1] <- NA
predict(mainEffects, when2[1:3,])
predict(mainEffects, when2[1:3,], na.action = na.omit)


interactionModel <- dummyVars(~ day + time + day:time,
                              data = when,
                              sep = ".")
predict(interactionModel, when[1:3,])

noNames <- dummyVars(~ day + time + day:time,
                     data = when,
                     levelsOnly = TRUE)
predict(noNames, when)

head(class2ind(iris$Species))

two_levels <- factor(rep(letters[1:2], each = 5))
class2ind(two_levels)
class2ind(two_levels, drop2nd = TRUE)