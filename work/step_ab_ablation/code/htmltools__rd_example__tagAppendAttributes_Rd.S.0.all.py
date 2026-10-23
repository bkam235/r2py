from bs4 import BeautifulSoup

# R: html <- div(a())
# r2py:entity:html
# We simulate the htmltools tag structure using BeautifulSoup
# div(a()) creates a div containing an a tag
soup = BeautifulSoup('<div class="root"><a></a></div>', 'html.parser')
html = soup.div

# R: tagAppendAttributes(html, class = "foo")
# r2py:entity:tagAppendAttributes
html['class'] = "foo"

# R: tagAppendAttributes(html, .cssSelector = "a", class = "bar")
# r2py:entity:tagAppendAttributes_1
# Find the element matching the CSS selector 'a' within html and add the class
target = html.select_one("a")
if target:
    target['class'] = "bar"

# R: tagAppendAttributes(html, contenteditable = NA)
# r2py:entity:tagAppendAttributes_2
# In R's htmltools, passing NA to tagAppendAttributes removes the attribute
if "contenteditable" in html.attrs:
    del html['contenteditable']

# R: tagHasAttribute(div(foo = "bar"), "foo")
# r2py:entity:tagHasAttribute
temp_soup = BeautifulSoup('<div foo="bar"></div>', 'html.parser')
div_foo_bar_1 = temp_soup.div
tagHasAttribute = "foo" in div_foo_bar_1.attrs

# R: tagGetAttribute(div(foo = "bar"), "foo")
# r2py:entity:tagGetAttribute
temp_soup2 = BeautifulSoup('<div foo="bar"></div>', 'html.parser')
div_foo_bar_2 = temp_soup2.div
tagGetAttribute = div_foo_bar_2.get("foo")