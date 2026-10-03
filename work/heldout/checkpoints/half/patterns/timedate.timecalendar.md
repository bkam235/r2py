---
id: timedate.timecalendar
package: timeDate
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# timedate.timecalendar

## Guidance
Translate R `timeCalendar` (FunctionCall from timeDate) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "688be16b", "r_snippet": "timeCalendar() ", "py_snippet": "def timeCalendar(y=None, m=None, d=None, h=None, min_val=None, s=None, zone=\"\", FinCenter=\"\"):\n    # Defaults\n    if y is None:\n        y = getRmetricsOptions(\"currentYear\")\n    if m is None:\n        m = list(range(1, 13))\n    if d is None:\n        d = [1]\n    if h is None:\n        h = [0]\n    if min_val is None:\n        min_val = [0]\n    if s is None:\n        s = [0]\n        \n    if zone == \"\":\n        zone = getRmetricsOptions(\"myFinCenter\")\n    if FinCenter == \"\":\n        FinCenter = getRmetricsOptions(\"myFinCenter\")\n        \n    # Recyling logic\n    # R uses length(m), length(d), etc.\n    # We ensure inputs are lists/arrays\n    m_list = np.atleast_1d(m)\n    d_list = np.atleast_1d(d)\n    y_list = np.atleast_1d(y)\n    h_list = np.atleast_1d(h)\n    min_list = np.atleast_1d(min_val)\n    s_list = np.atleast_1d(s)\n    \n    data_len = max(len(m_list), len(d_list), len(y_list), len(h_list), len(min_list), len(s_list))\n    \n    def recycle(arr, length):\n        if len(arr) == 0: return np.full(length, np.nan)\n        return np.resize(arr, length)\n\n    m_rec = recycle(m_list, data_len)\n    d_rec = recycle(d_list, data_len)\n    y_rec = recycle(y_list, data_len)\n    h_rec = recycle(h_list, data_len)\n    min_rec = recycle(min_list, data_len)\n    s_rec = recycle(s_list, data_len)\n    \n    tz = pytz.timezone(FinCenter if FinCenter else zone)\n    results = []\n    for i in range(data_len):\n        # Create naive datetime then localize\n        dt_naive = datetime(int(y_rec[i]), int(m_rec[i]), int(d_rec[i]), \n                            int(h_rec[i]), int(min_rec[i]), int(s_rec[i]))\n        dt_localized = tz.localize(dt_naive)\n        results.append(dt_localized)\n    \n    # To match R's output printing style (just the dates/times)\n    # In a real scenario, timeDate returns a specific class, but for stdout:\n    return results\n\n# Current Year:\n\nres_cal = timeCalendar()\nprint(f\"GMT\\n{['[' + d.strftime('%Y-%m-%d') + ']' for d in res_cal]}\")\n\n# ...", "score": 1.0, "script_id": "timeDate__rd_example__timeDate-Calendar_Rd", "n_calls": 0}

## Edit Examples
(none)
