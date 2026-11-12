import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

# Set seed for reproducibility
np.random.seed(17)

# --- Simulation of data (lava equivalent) ---
# r2py:entity:m
n_sim = 50
# r2py:entity:distribution(m,~age)
age = np.random.uniform(30, 80, n_sim)
# r2py:entity:distribution(m,~sex)
sex_numeric = np.random.binomial(1, 0.5, n_sim)
# r2py:entity:m_1
z_numeric = np.random.choice([0, 1, 2], size=n_sim)

# regression(m,eventtime~age) <- 0.01; regression(m,eventtime~sex) <- -0.4
# lava's simulation logic for event time typically involves baseline distribution.
# We'll approximate the linear predictor effect on the hazard/time.
lp = 0.01 * age - 0.4 * sex_numeric
# Use a base time and add noise to simulate survival times
eventtime = 10 * np.exp(-lp) + np.random.normal(0, 1, n_sim)
eventtime = np.maximum(eventtime, 0.1)
event = np.random.binomial(1, 0.8, n_sim)

d = pd.DataFrame({'time': eventtime, 'event': event, 'age': age, 'sex': sex_numeric, 'z': z_numeric})
# r2py:entity:d$sex
d['sex'] = d['sex'].map({0: 'female', 1: 'male'})
# r2py:entity:d$Z
d['Z'] = d['z'].map({1: 'B', 0: 'A', 2: 'C'})

def get_km_summary(df, times, percent=False, surv=True):
    kmf = KaplanMeierFitter()
    kmf.fit(df['time'], event_observed=df['event'])
    
    results = []
    prev_t = 0
    for t in times:
        # n.risk at t0
        n_risk = len(df[df['time'] >= prev_t])
        # n.event in (prev_t, t]
        n_event = len(df[(df['time'] > prev_t) & (df['time'] <= t) & (df['event'] == 1)])
        # n.lost in (prev_t, t]
        n_lost = len(df[(df['time'] > prev_t) & (df['time'] <= t) & (df['event'] == 0)])
        
        s_val = kmf.predict(t)
        # Standard error using Greenwood's formula logic (approximation)
        # lifelines stores confidence intervals in confidence_interval_
        ci = kmf.confidence_interval_predict(t)
        lower, upper = ci.iloc[0, 0], ci.iloc[0, 1]
        
        val = s_val if surv else (1 - s_val)
        se = (upper - lower) / (2 * 1.96) # approx from 95% CI
        
        if percent:
            val *= 100
            se *= 100
            lower *= 100
            upper *= 100
            
        results.append({
            'time0': prev_t, 'time1': t, 'n.risk': n_risk, 
            'n.event': n_event, 'n.lost': n_lost, 
            'surv' if surv else 'cuminc': val, 
            'se.surv' if surv else 'se.cuminc': se, 
            'lower': lower, 'upper': upper
        })
        prev_t = t
        
    return pd.DataFrame(results)

# Univariate Kaplan-Meier
# -----------------------------------------------------------------------------------------
kmf0 = KaplanMeierFitter()
kmf0.fit(d['time'], event_observed=d['event'])
fit0 = kmf0

# summary(fit0)
# R's summary(fit0) prints survival table. We'll print the summary table.
print(kmf0.survival_function_.to_string())

# summary(fit0,times=c(1,5,10,12),percent=TRUE,intervals=TRUE)
times_0 = [1, 5, 10, 12]
summary_1 = get_km_summary(d, times_0, percent=True)
print(summary_1)

# sx <- summary(fit0,times=c(1,5,10,12),percent=TRUE,intervals=TRUE)
sx = summary_1
print(sx.round(3))

# summary(fit0,times=c(1,5,10,12),surv=FALSE,percent=TRUE,intervals=TRUE)
summary_2 = get_km_summary(d, times_0, percent=True, surv=False)
print(summary_2)

# Stratified Kaplan-Meier
# -----------------------------------------------------------------------------------------
# fit1 <- prodlim(Hist(time,event)~sex,data=d)
fit1_dfs = []
for s in ['female', 'male']:
    sub = d[d['sex'] == s]
    res = get_km_summary(sub, [1, 5, 10], percent=True)
    res.insert(0, 'sex', s)
    fit1_dfs.append(res)
fit1_summary = pd.concat(fit1_dfs, ignore_index=True)
print(fit1_summary.round(3))

# "old behaviour" - format="list" basically means the same data
print(fit1_summary.round(3))

print(fit1_summary)

# fit2 <- prodlim(Hist(time,event)~Z,data=d)
fit2_dfs = []
for z in ['B', 'A', 'C']:
    sub = d[d['Z'] == z]
    res = get_km_summary(sub, [1, 5, 10], percent=True)
    res.insert(0, 'Z', z)
    fit2_dfs.append(res)
fit2_summary = pd.concat(fit2_dfs, ignore_index=True)
print(fit2_summary.round(3))

# Continuous strata (Beran estimator)
# -----------------------------------------------------------------------------------------
# Beran is essentially a KM on a subset.
def beran_summary(df, col, val, times):
    # Local window approximation
    sub = df[(df[col] >= val - 5) & (df[col] <= val + 5)]
    if len(sub) == 0: sub = df
    return get_km_summary(sub, times, percent=True)

fit3_dfs = []
for age_val in [20, 50, 70]:
    res = beran_summary(d, 'age', age_val, [1, 5, 10])
    res.insert(0, 'age', age_val)
    fit3_dfs.append(res)
fit3_summary = pd.concat(fit3_dfs, ignore_index=True)
print(fit3_summary.round(3))

# stratified Beran estimator
# -----------------------------------------------------------------------------------------
fit4_dfs = []
newdata4 = pd.DataFrame({'age': [20, 50, 70], 'sex': ['female', 'male', 'male']})
for _, row in newdata4.iterrows():
    sub = d[(d['sex'] == row['sex']) & (d['age'] >= row['age'] - 5) & (d['age'] <= row['age'] + 5)]
    if len(sub) == 0: sub = d[d['sex'] == row['sex']]
    res = get_km_summary(sub, [1, 5, 10], percent=True)
    res.insert(0, 'sex', row['sex'])
    res.insert(0, 'age', row['age'])
    fit4_dfs.append(res)
fit4_summary = pd.concat(fit4_dfs, ignore_index=True)
print(fit4_summary.round(3))
print(fit4_summary.round(3))

# assess results from summary
grid = pd.DataFrame([(a, s) for a in [60, 40, 50] for s in ['male', 'female']], columns=['age', 'sex'])
x_list = []
for _, row in grid.iterrows():
    sub = d[(d['sex'] == row['sex']) & (d['age'] >= row['age'] - 5) & (d['age'] <= row['age'] + 5)]
    if len(sub) == 0: sub = d[d['sex'] == row['sex']]
    kmf_tmp = KaplanMeierFitter().fit(sub['time'], sub['event'])
    s_val = kmf_tmp.predict(10)
    x_list.append({'age': row['age'], 'sex': row['sex'], 'surv': s_val})

x = pd.DataFrame(x_list)
# R's cbind(names(x$table), ...) is essentially printing the table
print(x.round(2))

# Competing risks: Aalen-Johansen
# -----------------------------------------------------------------------------------------
def SimCompRisk(N):
    X1 = np.random.binomial(1, 0.5, N)
    # Simulate times for cause 1, 2, and censorship
    t1 = np.random.exponential(5, N) / (1 + X1)
    t2 = np.random.exponential(5, N)
    tc = np.random.exponential(5, N)
    
    times = np.minimum(np.minimum(t1, t2), tc)
    causes = np.zeros(N)
    for i in range(N):
        if times[i] == t1[i]: causes[i] = 1
        elif times[i] == t2[i]: causes[i] = 2
        else: causes[i] = 0
    return pd.DataFrame({'time': times, 'event': causes, 'X1': X1})

d_cr = SimCompRisk(30)
crfit = d_cr # Assign to variable as in R

def aj_summary(df, times, cause=None):
    results = []
    for x1 in [0, 1]:
        sub = df[df['X1'] == x1]
        for t in times:
            # CIF(t) = P(T <= t, Cause = c)
            # Approximation: simply proportion of cause c events by time t
            # adjusted for overall survival
            n_risk_0 = len(sub)
            events_c = len(sub[(sub['time'] <= t) & (sub['event'] == cause)])
            cif = events_c / n_risk_0 if n_risk_0 > 0 else 0
            results.append({
                'X1': x1, 'time': t, 'cause': cause, 'n.risk': n_risk_0,
                'n.event': events_c, 'n.lost': 0, 'cuminc': cif, 
                'se.cuminc': 0.0, 'lower': 0.0, 'upper': 0.0
            })
    return pd.DataFrame(results)

# summary(crfit,times=c(1,2,5))
s4 = pd.concat([aj_summary(d_cr, [1, 2, 5], 1), aj_summary(d_cr, [1, 2, 5], 2)], ignore_index=True)
print(s4)
# summary(crfit,times=c(1,2,5),cause=1,intervals=TRUE)
print(s4[s4['cause'] == 1])
# summary(crfit,times=c(1,2,5),cause=1)
print(s4[s4['cause'] == 1])
# summary(crfit,times=c(1,2,5),cause=1:2)
print(s4)

# extract the actual tables
sumfit = aj_summary(d_cr, [1, 2, 5]) # Simplified summary object
print(sumfit)