---
id: base.plot_to_matplotlib
package: base
confidence: tentative
seed: true
created: 2026-06-01
last_review: 2026-06-01
---

# base.plot_to_matplotlib

## Guidance
R's base graphics functions (`plot`, `barplot`, `hist`, `boxplot`, `pie`, `lines`,
`points`, `abline`) translate to `matplotlib.pyplot`. Always add `import matplotlib.pyplot as plt`
at the top of the script.

### Common translations

```
plot(x, y)                      → plt.figure(); plt.plot(x, y); plt.show()
plot(x, y, type="l")            → plt.figure(); plt.plot(x, y); plt.show()
plot(x, y, xlab="X", ylab="Y") → plt.figure(); plt.plot(x, y); plt.xlabel("X"); plt.ylabel("Y"); plt.show()
barplot(heights)                → plt.figure(); plt.bar(range(len(heights)), heights); plt.show()
hist(x)                         → plt.figure(); plt.hist(x); plt.show()
hist(x, breaks=n)               → plt.figure(); plt.hist(x, bins=n); plt.show()
boxplot(x)                      → plt.figure(); plt.boxplot(x); plt.show()
pie(x)                          → plt.figure(); plt.pie(x); plt.show()
lines(x, y)                     → plt.plot(x, y)   # adds to existing figure
points(x, y)                    → plt.scatter(x, y)
abline(h=v)                     → plt.axhline(v)
abline(v=v)                     → plt.axvline(v)
```

### Date axes
When x is a date column (e.g. `df$date`), pass the pandas column directly —
matplotlib handles `datetime64` automatically:
```python
plt.plot(df['date'], df['value'])
```

### Inside _with_locale or other wrappers
When `plot(...)` appears as the code argument to `with_locale`, wrap it in a lambda:
```python
_with_locale({"LC_TIME": "es_ES"}, lambda: (plt.figure(), plt.plot(df['date'], df['value']), plt.show()))
```
Or extract it to a named function for clarity:
```python
def _do_plot():
    plt.figure()
    plt.plot(df['date'], df['value'])
    plt.show()

_with_locale({"LC_TIME": "es_ES"}, _do_plot)
```

### plt.show() placement
Call `plt.show()` once per logical figure, at the end of the plotting block.
Do NOT call it inside a loop unless each iteration creates a separate figure.

## Evidence
(none)

## Contradictions
(none)
