import numpy as np
import pandas as pd

# r2py:entity:x
def iso_year_week_day(year, week=None, day=None):
    """
    Mimics clock::iso_year_week_day.
    Returns a DataFrame simulating the clock_iso_year_week_day object.
    """
    year = np.atleast_1d(year)
    week = np.atleast_1d(week) if week is not None else None
    day = np.atleast_1d(day) if day is not None else None

    # Broadcast to common length
    max_len = max(len(year), 
                  len(week) if week is not None else 0, 
                  len(day) if day is not None else 0)
    
    def broadcast(arr, length):
        if arr is None:
            return np.full(length, 1)
        if len(arr) == 1:
            return np.full(length, arr[0])
        # Simple recycle/repeat logic similar to vec_recycle_common
        return np.resize(arr, length)

    years = broadcast(year, max_len)
    weeks = broadcast(week, max_len)
    days = broadcast(day, max_len)

    df = pd.DataFrame({'year': years, 'week': weeks, 'day': days})
    df.attrs['clock_class'] = 'clock_iso_year_week_day'
    df.attrs['precision'] = 'day'
    return df

# r2py:entity:calendar_group
def calendar_group(x, precision, n=1):
    """
    Mimics clock::calendar_group.
    Groups calendar objects by a specified precision and count.
    Returns a formatted representation of the grouped calendar.
    """
    if precision == "week":
        # R's calendar_group for weeks creates groups of n weeks.
        # The label is the start week of that group.
        years = x['year'].values
        weeks = x['week'].values
        
        # Create group identifiers based on index // n
        group_ids = np.arange(len(x)) // n
        
        # The label for the group is the ISO week of the first element in that group
        group_labels = []
        for i in range(len(x)):
            gid = i // n
            first_idx = gid * n
            lbl = f"{years[first_idx]}-W{weeks[first_idx]:02d}"
            group_labels.append(lbl)
            
        return np.array(group_labels)

    elif precision == "year":
        # Group by n years. 
        # The label is the year of the first element in that group.
        years = x['year'].values
        
        group_ids = np.arange(len(x)) // n
        
        group_labels = []
        for i in range(len(x)):
            gid = i // n
            first_idx = gid * n
            lbl = str(years[first_idx])
            group_labels.append(lbl)
            
        return np.array(group_labels)
    else:
        raise NotImplementedError(f"Precision {precision} not implemented")

# --- Translation of the script ---

# x <- iso_year_week_day(2019, 1:52)
# r2py:entity:x
x = iso_year_week_day(2019, np.arange(1, 53))

# Group by 3 ISO weeks
# calendar_group(x, "week", n = 3)
# r2py:entity:calendar_group
res_x = calendar_group(x, "week", n=3)
print(f" <iso_year_week_day<week>[{len(res_x)}]>")
print(res_x)

# y <- iso_year_week_day(2000:2020, 1, 1)
# r2py:entity:y
y = iso_year_week_day(np.arange(2000, 2021), 1, 1)

# Group by 2 ISO years
# calendar_group(y, "year", n = 2)
# r2py:entity:calendar_group_1
res_y = calendar_group(y, "year", n=2)
print(f" <iso_year_week_day<year>[{len(res_y)}]>")
print(res_y)