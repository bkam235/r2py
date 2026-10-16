import pandas as pd
from bs4 import BeautifulSoup
import io

# r2py:entity:suppressPackageStartupMessages
def suppressPackageStartupMessages(func):
    return func

# r2py:entity:import_rvest
# rvest is handled by the functions below

# To match the R object structure for sample1, sample2, sample3
class XMLDocument:
    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return f"XMLDocument(text={self.text!r})"

# r2py:entity:minimal_html
def minimal_html(html, title=""):
    # R's minimal_html creates a full XML document
    full_html = f'<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta charset="utf-8">\n<title>{title}</title>\n</head>\n<body>{html}</body>\n</html>'
    # We normalize whitespace in the table for consistency with pandas read_html
    return XMLDocument(full_html)

# r2py:entity:html_element
def html_element(x, css=None, xpath=None):
    # x is an XMLDocument, we need to parse it with BeautifulSoup to find the element
    soup = BeautifulSoup(x.text, "html.parser")
    if css:
        return soup.select_one(css)
    return soup

# r2py:entity:html_table
def html_table(x, header=None, trim=True, dec=".", na_strings="NA", convert=True):
    # Convert the BeautifulSoup element to a string
    html_str = str(x)
    dfs = pd.read_html(io.StringIO(html_str), decimal=dec)
    
    if not dfs:
        return pd.DataFrame()
    
    df = dfs[0]
    
    if header is False:
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        
    if na_strings != "NA":
        df = df.replace(na_strings, pd.NA)
        
    if convert:
        # R's html_table converts to numeric if possible.
        # We use pd.to_numeric and then convert to Int64 (nullable integer) to match R's <int> output
        for col in df.columns:
            try:
                converted = pd.to_numeric(df[col])
                # Check if it's actually integers (no decimals)
                if (converted % 1 == 0).all():
                    df[col] = converted.astype('Int64')
                else:
                    df[col] = converted
            except (ValueError, TypeError):
                pass
                
    return df

# Sample 1
# r2py:entity:sample1
sample1 = minimal_html("<table>\n  <tr><th>Col A</th><th>Col B</th></tr>\n  <tr><td>1</td><td>x</td></tr>\n  <tr><td>4</td><td>y</td></tr>\n  <tr><td>10</td><td>z</td></tr>\n</table>")
# r2py:entity:html_element
res1 = html_element(sample1, css="table")
# r2py:entity:html_table
res1 = html_table(res1)
print(res1.to_string(index=False))

# Values in merged cells will be duplicated
# r2py:entity:sample2
sample2 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td>1</td><td>2</td><td>3</td></tr>\n  <tr><td colspan='2'>4</td><td>5</td></tr>\n  <tr><td>6</td><td colspan='2'>7</td></tr>\n</table>")
# r2py:entity:html_element_1
res2 = html_element(sample2, css="table")
# r2py:entity:html_table_1
res2 = html_table(res2)
print(res2.to_string(index=False))

# If a row is missing cells, they'll be filled with NAs
# r2py:entity:sample3
sample3 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td colspan='2'>1</td><td>2</td></tr>\n  <tr><td colspan='2'>3</td></tr>\n  <tr><td>4</td></tr>\n</table>")
# r2py:entity:html_element_2
res3 = html_element(sample3, css="table")
# r2py:entity:html_table_2
res3 = html_table(res3)
print(res3.to_string(index=False))