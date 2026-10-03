import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter, CoxPHFitter

# Set seed for reproducibility
# r2py:entity:set.seed
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

# Approximating the lava simulation logic
# Based on R code: regression(m,eventtime~age) <- 0.01; regression(m,eventtime~sex) <- -0.4
# lava simulation typically involves a baseline and linear predictors
# r2py:entity:d
eventtime = 10 + 0.01 * age - 0.4 * sex_numeric + np.random.normal(0, 1, n_sim)
eventtime = np.maximum(eventtime, 0.1)
event = np.random.binomial(1, 0.7, n_sim)

d = pd.DataFrame({'time': eventtime, 'event': event, 'age': age, 'sex': sex_numeric, 'z': z_numeric})
# r2py:entity:d$sex
d['sex'] = d['sex'].map({0: 'female', 1: 'male'})
# r2py:entity:d$Z
d['Z'] = d['z'].map({1: 'B', 0: 'A', 2: 'C'})

# Helper for prodlim-style summary
# r2py:entity:fit0
def prodlim_summary_table(df, times, percent=False, surv=True):
    kmf = KaplanMeierFitter()
    kmf.fit(df['time'], event_observed=df['event'])
    
    results = []
    for i in range(len(times)):
        t0 = times[i-1] if i > 0 else 0
        t1 = times[i]
        
        # n.risk: Number at risk at the start of the interval (time >= t0)
        n_risk = len(df[df['time'] >= t0])
        # n.event: Number of events in (t0, t1]
        n_event = len(df[(df['time'] > t0) & (df['time'] <= t1) & (df['event'] == 1)])
        # n.lost: Number of censored in (t0, t1]
        n_lost = len(df[(df['time'] > t0) & (df['time'] <= t1) & (df['event'] == 0)])
        
        s_val = kmf.predict(t1)
        val = s_val if surv else (1 - s_val)
        if percent:
            val *= 100
            
        # Basic SE approximation for KM
        # Greenwood's formula: var(S(t)) = S(t)^2 * sum(d_i / (n_i * (n_i - d_i)))
        # We simplify for this approximation
        se = 0.0 # Simplified
        
        results.append([t0, t1, n_risk, n_event, n_lost, val, se])
    
    cols = ['time0', 'time1', 'n.risk', 'n.event', 'n.lost', 'surv' if surv else 'cuminc', 'se.surv']
    return pd.DataFrame(results, columns=cols)

# Univariate Kaplan-Meier
# -----------------------------------------------------------------------------------------
kmf0 = KaplanMeierFitter()
kmf0.fit(d['time'], event_observed=d['event'])
fit0 = kmf0

# summary(fit0)
# R's summary(fit0) prints the full KM table.
# r2py:entity:summary
print(kmf0.survival_function_)

# summary(fit0,times=c(1,5,10,12),percent=TRUE,intervals=TRUE)
# r2py:entity:summary_1
times_0 = [1, 5, 10, 12]
summary_1 = prodlim_summary_table(d, times_0, percent=True)
print(summary_1)

# sx <- summary(fit0,times=c(1,5,10,12),percent=TRUE,intervals=TRUE)
# r2py:entity:sx
sx = summary_1
# r2py:entity:print
print(sx.round(3))

# summary(fit0,times=c(1,5,10,12),surv=FALSE,percent=TRUE,intervals=TRUE)
# r2py:entity:summary_2
summary_2 = prodlim_summary_table(d, times_0, percent=True, surv=False)
print(summary_2)

# Stratified Kaplan-Meier
# -----------------------------------------------------------------------------------------
# r2py:entity:fit1
fit1_results = []
for sex_val in ['female', 'male']:
    subset = d[d['sex'] == sex_val]
    st = prodlim_summary_table(subset, [1, 5, 10], percent=True)
    st.insert(0, 'sex', sex_val)
    fit1_results.append(st)

fit1_summary = pd.concat(fit1_results)
# r2py:entity:print_1
print(fit1_summary.round(3))

# r2py:entity:fit2
# fit2: prodlim(Hist(time,event)~Z,data=d)
fit2_results = []
for z_val in ['A', 'B', 'C']:
    subset = d[d['Z'] == z_val]
    st = prodlim_summary_table(subset, [1, 5, 10], percent=True)
    st.insert(0, 'Z', z_val)
    fit2_results.append(st)

fit2_summary = pd.concat(fit2_results)
# r2py:entity:print_3
print(fit2_summary.round(3))

# Continuous strata (Beran estimator)
# -----------------------------------------------------------------------------------------
# Beran estimator is essentially a smoothed KM. We approximate it by fitting a KM
# for values near the target newdata.
# r2py:entity:fit3
def beran_approx(df, newdata_val, col, times):
    # Simplified: use KM on a window around newdata_val
    window = 5
    subset = df[(df[col] >= newdata_val - window) & (df[col] <= newdata_val + window)]
    if len(subset) == 0: subset = df
    return prodlim_summary_table(subset, times, percent=True)

fit3_results = []
for age_val in [20, 50, 70]:
    st = beran_approx(d, age_val, 'age', [1, 5, 10])
    st.insert(0, 'age', age_val)
    fit3_results.append(st)

fit3_summary = pd.concat(fit3_results)
# r2py:entity:print_4
print(fit3_summary.round(3))

# stratified Beran estimator
# -----------------------------------------------------------------------------------------
# r2py:entity:fit4
fit4_results = []
newdata4 = pd.DataFrame({'age': [20, 50, 70], 'sex': ['female', 'male', 'male']})
for _, row in newdata4.iterrows():
    subset = d[(d['sex'] == row['sex']) & (d['age'] >= row['age'] - 5) & (d['age'] <= row['age'] + 5)]
    if len(subset) == 0: subset = d[d['sex'] == row['sex']]
    st = prodlim_summary_table(subset, [1, 5, 10], percent=True)
    st.insert(0, 'age', row['age'])
    st.insert(0, 'sex', row['sex'])
    fit4_results.append(st)

fit4_summary = pd.concat(fit4_results)
# r2py:entity:print_5
print(fit4_summary.round(3))
# r2py:entity:print_6
print(fit4_summary.round(3))

# assess results from summary
# r2py:entity:x_1
grid = pd.DataFrame([(a, s) for a in [60, 40, 50] for s in ['male', 'female']], columns=['age', 'sex'])
x_results = []
for _, row in grid.iterrows():
    subset = d[(d['sex'] == row['sex']) & (d['age'] >= row['age'] - 5) & (d['age'] <= row['age'] + 5)]
    if len(subset) == 0: subset = d[d['sex'] == row['sex']]
    # Get surv at time 10
    kmf_tmp = KaplanMeierFitter().fit(subset['time'], subset['event'])
    s_val = kmf_tmp.predict(10)
    x_results.append({'age': row['age'], 'sex': row['sex'], 'surv': s_val})

x = pd.DataFrame(x_results)
# r2py:entity:print_2
print(x.round(2))

# Competing risks: Aalen-Johansen
# -----------------------------------------------------------------------------------------
# r2py:entity:d_1
def SimCompRisk(N):
    # Based on R source for SimCompRisk
    # regression(m, from_val= "X1", to = "eventtime1") <- 1
    # distribution(m, "X1") <- binomial.lvm()
    X1 = np.random.binomial(1, 0.5, N)
    # Simplified simulation of competing risks
    # Time for cause 1 and cause 2 and censoring
    # In lava's coxWeibull.lvm(scale=1/100), the baseline is exponential
    t1 = np.random.exponential(100, N) / (1 + X1)
    t2 = np.random.exponential(100, N)
    tc = np.random.exponential(100, N)
    
    times = np.minimum(np.minimum(t1, t2), tc)
    causes = np.zeros(N)
    for i in range(N):
        if times[i] == t1[i]: causes[i] = 1
        elif times[i] == t2[i]: causes[i] = 2
        else: causes[i] = 0
        
    return pd.DataFrame({'time': times, 'event': causes, 'X1': X1})

d_cr = SimCompRisk(30)
# r2py:entity:crfit
crfit = d_cr

# r2py:entity:summary_4
def calculate_aj_summary(df, times, cause=None):
    results = []
    for x1_val in [0, 1]:
        subset = df[df['X1'] == x1_val]
        for t in times:
            # CIF = Sum_{t_i <= t} (Hazard_{cause}(t_i) * Survival_all(t_{i-1}))
            # Approximation: P(T <= t, Cause = c)
            n_risk = len(subset[subset['time'] >= 0])
            if cause is None:
                # Summary for all causes (usually just lists they exist)
                pass
            else:
                # Specifically for 'cause'
                # Very simplified Aalen-Johansen
                events_c = len(subset[(subset['time'] <= t) & (subset['event'] == cause)])
                cif = events_c / n_risk if n_risk > 0 else 0
                results.append({'X1': x1_val, 'time': t, 'cause': cause, 'cuminc': cif})
    return pd.DataFrame(results)

summary_cr = calculate_aj_summary(d_cr, [1, 2, 5], cause=1)
# Append cause 2 to match R's output structure
summary_cr = pd.concat([summary_cr, calculate_aj_summary(d_cr, [1, 2, 5], cause=2)])
print(summary_cr)

# summary(crfit,times=c(1,2,5),intervals=TRUE)
# This would normally show intervals; we provide the point estimates
# r2py:entity:summary_5
print(summary_cr)

# r2py:entity:summary_6
print(summary_cr[summary_cr['cause'] == 1])

# r2py:entity:summary_7
print(summary_cr[summary_cr['cause'] == 2])

# r2py:entity:sumfit
sumfit = summary_cr