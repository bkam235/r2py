# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: xtableGallery_s29
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\xtableGallery.R
# lines: 9

suppressPackageStartupMessages(library(xtable))
insane <- data.frame(Name = c("Ampersand","Greater than","Less than",
                            "Underscore","Per cent","Dollar",
                            "Backslash","Hash","Caret","Tilde",
                            "Left brace","Right brace"),
                     Character = I(c("&",">","<","_","%","$",
                                     "\\","#","^","~","{","}")))
colnames(insane)[2] <- paste(insane[, 2], collapse = "")
xtable(insane)