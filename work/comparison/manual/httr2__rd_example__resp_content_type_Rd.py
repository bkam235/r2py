# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: resp_content_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 9

from httpx import Response

resp = Response(200, headers={"Content-Type": "text/html; charset=utf-8"})
print(resp.headers["content-type"].split(";")[0].strip())
print(resp.encoding)

# No Content-Type header
resp = Response(200)
print(resp.headers.get("content-type", ""))
print(resp.encoding)
