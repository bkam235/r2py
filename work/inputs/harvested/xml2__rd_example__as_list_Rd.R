# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: as_list.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 5

suppressPackageStartupMessages(library(xml2))
as_list(read_xml("<foo> a <b /><c><![CDATA[<d></d>]]></c></foo>"))
as_list(read_xml("<foo> <bar><baz /></bar> </foo>"))
as_list(read_xml("<foo id = 'a'></foo>"))
as_list(read_xml("<foo><bar id='a'/><bar id='b'/></foo>"))