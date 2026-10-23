import pandas as pd
from bs4 import BeautifulSoup
import io
import numpy as np

# r2py:entity:minimal_html
def minimal_html(html, title=""):
    full_html = f"<!doctype html>\n<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n<meta charset=\"utf-8\">\n<title>{title}</title>\n</head>\n<body>{html}</body>\n</html>"
    return BeautifulSoup(full_html, "html.parser")

# r2py:entity:html_element
def html_element(x, css=None, xpath=None):
    if css:
        return x.select_one(css)
    if xpath:
        raise NotImplementedError("XPath not implemented in this translation.")
    return x

# r2py:entity:html_table
def html_table(x, header=True, trim=True, dec=".", na_strings="NA", convert=True):
    if x is None:
        return pd.DataFrame()
    
    table = x if x.name == 'table' else x.find('table')
    if not table:
        return pd.DataFrame()

    rows = table.find_all('tr')
    data = []
    
    for tr in rows:
        row_data = []
        # Handle colspan/rowspan by tracking current row cells
        cells = tr.find_all(['td', 'th'])
        
        # Note: a full implementation of rowspan is complex; 
        # but rvest's example focuses on colspan and missing cells.
        # We simulate the "merged cells will be duplicated" behavior.
        curr_col = 0
        # This is a simplification for colspan
        for cell in cells:
            val = cell.get_text(strip=trim)
            colspan = int(cell.get('colspan', 1))
            for _ in range(colspan):
                row_data.append(val)
        data.append(row_data)

    if not data:
        return pd.DataFrame()

    # Find max columns to pad rows (R's html_table fills missing cells with NA)
    max_cols = max(len(row) for row in data)
    for row in data:
        while len(row) < max_cols:
            row.append(np.nan)

    df = pd.DataFrame(data)
    
    if header:
        # Use the first row as header
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
    else:
        df.columns = [f"V{i+1}" for i in range(df.shape[1])]

    if na_strings != "NA":
        df = df.replace(na_strings, np.nan)
    
    if convert:
        # R's html_table attempts to convert to numeric. 
        # We use pd.to_numeric and keep as object/float to allow NaNs, 
        # then Int64 for integer-like columns to match tibble output.
        for col in df.columns:
            converted = pd.to_numeric(df[col], errors='ignore')
            if pd.api.types.is_numeric_dtype(converted):
                # If all non-NaNs are integers, use Int64
                if converted.dropna().astype(float).mod(1).sum() == 0:
                    df[col] = converted.astype('Int64')
                else:
                    df[col] = converted
            else:
                df[col] = converted

    return df

# Sample 1
# r2py:entity:sample1
sample1 = minimal_html("<table>\n  <tr><th>Col A</th><th>Col B</th></tr>\n  <tr><td>1</td><td>x</td></tr>\n  <tr><td>4</td><td>y</td></tr>\n  <tr><td>10</td><td>z</td></tr>\n</table>")
res1 = html_element(sample1, css="table")
res1 = html_table(res1)
print(res1.to_string(index=False))

# Values in merged cells will be duplicated
# r2py:entity:sample2
sample2 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td>1</td><td>2</td><td>3</td></tr>\n  <tr><td colspan='2'>4</td><td>5</td></tr>\n  <tr><td>6</td><td colspan='2'>7</td></tr>\n</table>")
res2 = html_element(sample2, css="table")
res2 = html_table(res2)
print(res2.to_string(index=False))

# If a row is missing cells, they'll be filled with NAs
# r2py:entity:sample3
sample3 = minimal_html("<table>\n  <tr><th>A</th><th>B</th><th>C</th></tr>\n  <tr><td colspan='2'>1</td><td>2</td></tr>\n  <tr><td colspan='2'>3</td></tr>\n  <tr><td>4</td></tr>\n</table>")
res3 = html_element(sample3, css="table")
res3 = html_table(res3)
print(res3.to_string(index=False))