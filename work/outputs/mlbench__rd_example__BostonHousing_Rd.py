# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/mlbench__rd_example__BostonHousing_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'mlbench__rd_example__BostonHousing_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['BostonHousing', 'BostonHousing2']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:summary
def r_summary(df):
    """
    Mimics R's summary() output for data frames.
    """
    all_cols = list(df.columns)
    num_cols_total = len(all_cols)
    cols_per_page = 5
    
    for page in range(0, num_cols_total, cols_per_page):
        chunk_cols = all_cols[page : page + cols_per_page]
        
        # R's header: column names aligned
        header_line = " "
        for col in chunk_cols:
            header_line += f"{col:>15} "
        print(header_line)
        
        # Gather statistics for this chunk
        col_data = {}
        max_rows = 0
        
        for col in chunk_cols:
            series = df[col]
            # Check if it's numeric
            if pd.api.types.is_numeric_dtype(series):
                # R's summary for numeric: Min, 1st Qu, Median, Mean, 3rd Qu, Max
                # Using .5g to match R's general formatting
                stats = [
                    f"Min.   : {series.min():.5g}",
                    f"1st Qu.: {series.quantile(0.25):.5g}",
                    f"Median : {series.median():.5g}",
                    f"Mean   : {series.mean():.5g}",
                    f"3rd Qu.: {series.quantile(0.75):.5g}",
                    f"Max.   : {series.max():.5g}"
                ]
                col_data[col] = stats
                max_rows = max(max_rows, 6)
            else:
                # Factor/Categorical
                counts = series.value_counts()
                # R's summary for factors often shows levels sorted by count descending
                sorted_counts = counts.sort_values(ascending=False)
                
                stats = []
                # For binary/small sets, R prints "0:X, 1:Y"
                # For larger sets, it lists top ones then "(Other levels: N)"
                # Based on verification: BostonHousing's 'chas' shows "0:471\n1: 35"
                
                # If it's a small number of unique values (like chas), show all
                if len(counts) <= 6:
                    # Sort by index to match R's level order for small factors usually
                    idx_sorted = counts.sort_index()
                    for lvl, count in idx_sorted.items():
                        stats.append(f"{str(lvl):>13} : {count:>3}")
                else:
                    # For 'town' in BostonHousing2
                    top_levels = sorted_counts.head(6)
                    for lvl, count in top_levels.items():
                        stats.append(f"{str(lvl):>15} : {count:>3}")
                    
                    other_count = len(counts) - 6
                    if other_count > 0:
                        stats.append(f" (Other levels: {other_count})")
                
                col_data[col] = stats
                max_rows = max(max_rows, len(stats))

        # Print rows
        for row_idx in range(max_rows):
            row_line = " "
            for col in chunk_cols:
                stats = col_data[col]
                if row_idx < len(stats):
                    # R's spacing is roughly 15-16 chars per column
                    row_line += f"{stats[row_idx]:<16} "
                else:
                    row_line += " " * 17
            print(row_line)

# suppressPackageStartupMessages(library(mlbench))
# library(mlbench) handled by shim

# data("BostonHousing", package = "mlbench")
# r2py:entity:data
BostonHousing_df = pd.DataFrame(BostonHousing)
# r2py:entity:summary
r_summary(BostonHousing_df)

# data("BostonHousing2", package = "mlbench")
# r2py:entity:data_1
BostonHousing2_df = pd.DataFrame(BostonHousing2)
# r2py:entity:summary_1
r_summary(BostonHousing2_df)