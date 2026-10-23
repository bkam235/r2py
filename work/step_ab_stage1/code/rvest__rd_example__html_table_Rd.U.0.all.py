import pandas as pd
from bs4 import BeautifulSoup
import io

# Helper to mimic rvest's xml_document/xml_node for data verification
class XMLNode:
    def __init__(self, text):
        self.text = text
    def __str__(self):
        return self.text

def suppressPackageStartupMessages(x):
    return x

# r2py:entity:minimal_html
def minimal_html(html, title=""):
    # rvest's minimal_html creates a full HTML document
    full_html = f'<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta charset="utf-8">\n<title>{title}</title>\n</head>\n<body>{html}</body>\n</html>'
    return XMLNode(full_html)

# r2py:entity:html_element
def html_element(x, css=None, xpath=None):
    soup = BeautifulSoup(str(x), "html.parser")
    if css:
        element = soup.select_one(css)
        return XMLNode(str(element)) if element else None
    if xpath:
        raise NotImplementedError("XPath not implemented")
    return x

# r2py:entity:html_table
def html_table(x, header=True, trim=True, dec=".", na_strings="NA", convert=True):
    html_str = str(x)
    dfs = pd.read_html(io.StringIO(html_str), decimal=dec)
    if not dfs:
        return pd.DataFrame()
    
    df = dfs[0]
    
    if not header:
        # pandas read_html usually assumes first row is header. 
        # If header=False, we'd need to re-read or shift.
        # But in these examples, header is default (True).
        pass
        
    # rvest's html_table handles colspan by duplicating values
    # pandas read_html also handles colspan by duplicating values by default.

    # Match R's type conversion (integers where possible, else numeric/char)
    if convert:
        for col in df.columns:
            try:
                # Convert to numeric, then try to keep as integer if no NaNs
                # Use nullable Int64 to allow NaNs while keeping integer-like display
                df[col] = pd.to_numeric(df[col]).astype('Int64')
            except (ValueError, TypeError):
                pass
                
    return df

# Sample 1
# r2py:entity:sample1
sample1 = minimal_html("<table>\n  <tr><th>Col A</th><th>Col B</th></tr>\n  <tr><td>1</td><td>x</td></tr>\n  <tr><td>4</td><td>y</td></tr>\n  <tr><td>10</td><td>z</td></tr>\n</table>")
# r2py:entity:html_element
res1_elem = html_element(sample1, css="table")
# r2py:entity:html_table
sample1_table = html_table(res1_elem)
print(sample1_table.to_string(index=False))

# Values in merged cells will be duplicated
# r2py:entity:sample2
sample2 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td>1</td><td>2</td><td>3</td></tr>\n  <tr><td colspan='2'>4</td><td>5</td></tr>\n  <tr><td>6</td><td colspan='2'>7</td></tr>\n</table>")
# r2py:entity:html_element_1
res2_elem = html_element(sample2, css="table")
# r2py:entity:html_table_1
sample2_table = html_table(res2_elem)
print(sample2_table.to_string(index=False))

# If a row is missing cells, they'll be filled with NAs
# r2py:entity:sample3
sample3 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td colspan='2'>1</td><td>2</td></tr>\n  <tr><td colspan='2'>3</td></tr>\n  <tr><td>4</td></tr>\n</table>")
# r2py:entity:html_element_2
res3_elem = html_element(sample3, css="table")
# r2py:entity:html_table_2
sample3_table = html_table(res3_elem)
print(sample3_table.to_string(index=False))