# r2py crawler metadata
# package: mime
# source_type: rd_example
# topic: guess_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\mime\help
# lines: 21

library(mime)
# well-known file types
guess_type(c("a/b/c.html", "d.pdf", "e.odt", "foo.docx", "tex"))
# not in the standard table, but in mimeextra
guess_type(c("a.md", "b.R"), mime_extra = NULL)
guess_type(c("a.md", "b.R"))

# override the standard MIME table (tex is text/x-tex by default)
guess_type("tex", mime_extra = c(tex = "text/plain"))
# unknown extension 'zzz'
guess_type("foo.zzz")
# force unknown types to be plain text
guess_type("foo.zzz", unknown = "text/plain")

# empty file extension
guess_type("Makefile")
# we know it is a plain text file
guess_type("Makefile", empty = "text/plain")

# subtypes
guess_type(c("abc.html", "def.htm"), subtype = c("charset=UTF-8", ""))