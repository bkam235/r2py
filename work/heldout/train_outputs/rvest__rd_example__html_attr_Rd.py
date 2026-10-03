from bs4 import BeautifulSoup

# r2py:entity:html
html_content = '<ul>\n  <li><a href="https://a.com" class_val="important">a</a></li>\n  <li class_val="active"><a href="https://c.com">b</a></li>\n  <li><a href="https://c.com">b</a></li>\n  </ul>'
# minimal_html adds a doctype and basic structure, though for bs4 it's often optional
# but to be precise with the R minimal_html function logic:
full_html = f"<!doctype html>\n<meta charset=utf-8>\n<title></title>\n{html_content}"
html = BeautifulSoup(full_html, 'html.parser')

# html |> html_elements("a") |> html_attrs()
# r2py:entity:html_attrs
html_attrs = [a.attrs for a in html.select("a")]

# html |> html_elements("a") |> html_attr("href")
# r2py:entity:html_attr
html_attr = [a.get("href") for a in html.select("a")]

# html |> html_elements("li") |> html_attr("class")
# r2py:entity:html_attr_1
html_attr_1 = [li.get("class") for li in html.select("li")]

# html |> html_elements("li") |> html_attr("class", default = "inactive")
# r2py:entity:html_attr_2
html_attr_2 = [li.get("class", "inactive") for li in html.select("li")]