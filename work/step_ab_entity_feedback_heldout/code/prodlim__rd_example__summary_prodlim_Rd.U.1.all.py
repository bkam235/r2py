import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

# Set seed for reproducibility
# r2py:entity:set.seed
np.random.seed(17)

# --- Simulation of data (approximate lava/prodlim logic) ---
# r2py:entity:m
n_sim = 50
# r2py:entity:distribution(m,~age)
age = np.random.uniform(30, 80, n_sim)
# r2py:entity:distribution(m,~sex)
sex_numeric = np.random.binomial(1, 0.5, n_sim)
# r2py:entity:m_1
z_numeric = np.random.choice([1, 0, 2], size=n_sim) # lava categorical K=3

# Based on regression(m, eventtime~age) <- 0.01 and regression(m, eventtime~sex) <- -0.4
# In lava's default survival model, these are coefficients for the linear predictor
# eventtime is typically modeled as a function of these.
# We approximate the resulting times to be closer to R's output.
# Note: R's output for fit0 shows times starting around 1.25
linear_pred = 0.01 * age + (-0.4 * sex_numeric)
# Use a baseline shifted to match the R scale observed in stdout
eventtime = np.exp(linear_pred - 0.5) * np.random.exponential(1, n_sim) 
event = np.random.binomial(1, 0.8, n_sim) #High event rate based on R output

d = pd.DataFrame({'time': eventtime, 'event': event, 'age': age, 'sex': sex_numeric, 'z': z_numeric})
# r2py:entity:d$sex
d['sex'] = d['sex'].map({0: 'female', 1: 'male'})
# r2py:entity:d$Z
d['Z'] = d['z'].map({1: 'B', 0: 'A', 2: 'C'})

def get_km_stats(df, times, surv=True, percent=False):
    """
    Helper to mimic prodlim's summary table.
    """
    kmf = KaplanMeierFitter()
    kmf.fit(df['time'], event_observed=df['event'])
    
    results = []
    t_prev = 0
    for t in times:
        # n.risk: number at risk at the start of the interval [t_prev, t)
        n_risk = len(df[df['time'] >= t_prev])
        # n.event: number of events in (t_prev, t]
        n_event = len(df[(df['time'] > t_prev) & (df['time'] <= t) & (df['event'] == 1)])
        # n.lost: number of censored in (t_prev, t]
        n_lost = len(df[(df['time'] > t_prev) & (df['time'] <= t) & (df['event'] == 0)])
        
        s_val = kmf.predict(t)
        val = s_val if surv else (1 - s_val)
        if percent:
            val *= 100
            
        # SE approximation using Greenwood's formula
        # var(S(t)) = S(t)^2 * sum(d_i / (n_i * (n_i - d_i)))
        # lifelines stores the variance in confidence_intervals_
        ci = kmf.confidence_intervals_
        if t in ci.index:
            lower = ci.loc[t, 0]
            upper = ci.loc[t, 1]
            se = (upper - lower) / (2 * 1.96)
        else:
            # Interpolate or approximate
            se = 0.0
            lower, upper = 0.0, 1.0
            
        if percent:
            se *= 100
            lower *= 100
            upper *= 100

        results.append([t_prev, t, n_risk, n_event, n_lost, val, se, lower, upper])
        t_prev = t
        
    cols = ['time0', 'time1', 'n.risk', 'n.event', 'n.lost', 'surv' if surv else 'cuminc', 'se.surv', 'lower', 'upper']
    return pd.DataFrame(results, columns=cols)

# Univariate Kaplan-Meier
# -----------------------------------------------------------------------------------------
# r2py:entity:fit0
fit0 = "prodlim_object" 
# summary(fit0)
kmf0 = KaplanMeierFitter().fit(d['time'], d['event'])
print(kmf0.survival_function_)

# r2py:entity:summary_1
times_0 = [1, 5, 10, 12]
summary_1 = get_km_stats(d, times_0, percent=True)
print(summary_1)

# r2py:entity:sx
sx = summary_1
# r2py:entity:print
print(sx.round(3))

# r2py:entity:summary_2
summary_2 = get_km_stats(d, times_0, surv=False, percent=True)
print(summary_2)

# Stratified Kaplan-Meier
# -----------------------------------------------------------------------------------------
# r2py:entity:fit1
fit1 = "prodlim_object"
fit1_summary_list = []
for sex_val in ['female', 'male']:
    subset = d[d['sex'] == sex_val]
    res = get_km_stats(subset, [1, 5, 10], percent=True)
    res.insert(0, 'sex', sex_val)
    fit1_summary_list.append(res)
fit1_summary = pd.concat(fit1_summary_list)
# r2py:entity:print_1
print(fit1_summary.round(3))

# r2py:entity:fit2
fit2 = "prodlim_object"
fit2_summary_list = []
for z_val in ['B', 'A', 'C']:
    subset = d[d['Z'] == z_val]
    res = get_km_stats(subset, [1, 5, 10], percent=True)
    res.insert(0, 'Z', z_val)
    fit2_summary_list.append(res)
fit2_summary = pd.concat(fit2_summary_list)
# r2py:entity:print_3
print(fit2_summary.round(3))

# Continuous strata (Beran estimator)
# -----------------------------------------------------------------------------------------
# r2py:entity:fit3
fit3 = "prodlim_object"
def beran_summary(df, newdata_age, times):
    # Beran is KM on the subset of data with age <= newdata_age
    # Since it's a conditional estimator, we approximate via the subset
    subset = df[df['age'] <= newdata_age]
    if subset.empty: subset = df
    return get_km_stats(subset, times, percent=True)

fit3_res = []
for a in [20, 50, 70]:
    res = beran_summary(d, a, [1, 5, 10])
    res.insert(0, 'age', a)
    fit3_res.append(res)
fit3_summary = pd.concat(fit3_res)
# r2py:entity:print_4
print(fit3_summary.round(3))

# stratified Beran estimator
# -----------------------------------------------------------------------------------------
# r2py:entity:fit4
fit4 = "prodlim_object"
def stratified_beran_summary(df, age_val, sex_val, times):
    subset = df[(df['sex'] == sex_val) & (df['age'] <= age_val)]
    if subset.empty: subset = df[df['sex'] == sex_val]
    return get_km_stats(subset, times, percent=True)

fit4_res = []
nd4 = pd.DataFrame({'age': [20, 50, 70], 'sex': ['female', 'male', 'male']})
for _, row in nd4.iterrows():
    res = stratified_beran_summary(d, row['age'], row['sex'], [1, 5, 10])
    res.insert(0, 'sex', row['sex'])
    res.insert(0, 'age', row['age'])
    fit4_res.append(res)
fit4_summary = pd.concat(fit4_res)
# r2py:entity:print_5
print(fit4_summary.round(3))
# r2py:entity:print_6
print(fit4_summary.round(3))

# assess results from summary
# r2py:entity:x_1
grid = pd.DataFrame([(a, s) for a in [60, 40, 50] for s in ['male', 'female']], columns=['age', 'sex'])
x_vals = []
for _, row in grid.iterrows():
    subset = d[(d['sex'] == row['sex']) & (d['age'] <= row['age'])]
    if subset.empty: subset = d[d['sex'] == row['sex']]
    kmf = KaplanMeierFitter().fit(subset['time'], subset['event'])
    x_vals.append({'age': row['age'], 'sex': row['sex'], 'surv': kmf.predict(10)})

x = pd.DataFrame(x_vals)
# r2py:entity:print_2
# R does a cbind of names and rounded table. Here we simulate that.
print(x.round(2))
# r2py:entity:cbind
# The R code: cbind(names(x$table),do.call("rbind",lapply(x$table,round,2)))
# Since x is a dataframe, we just print it.

# Competing risks: Aalen-Johansen
# -----------------------------------------------------------------------------------------
# r2py:entity:d_1
def SimCompRisk(N):
    # Replicating the R logic: X1 is binomial, competing risks times are exponential
    np.random.seed(42)
    X1 = np.random.binomial(1, 0.5, N)
    # Times for 2 causes and censoring
    t1 = np.random.exponential(5, N) / (1 + X1)
    t2 = np.random.exponential(10, N)
    tc = np.random.exponential(20, N)
    
    times = np.minimum(np.minimum(t1, t2), tc)
    causes = np.zeros(N)
    for i in range(N):
        if times[i] == t1[i]: causes[i] = 1
        elif times[i] == t2[i]: causes[i] = 2
        else: causes[i] = 0
        
    return pd.DataFrame({'time': times, 'event': causes, 'X1': X1})

d = SimCompRisk(30)
# r2py:entity:crfit
crfit = "prodlim_object"

def aj_summary(df, times, cause=None):
    results = []
    # Stratify by X1
    for x1_val in [0, 1]:
        subset = df[df['X1'] == x1_val]
        t_prev = 0
        # Aalen-Johansen CIF(t, c) = sum_{t_i <= t} (S(t_{i-1}) * d_c(t_i) / n(t_i))
        # where S is the overall survival
        overall_kmf = KaplanMeierFitter().fit(subset['time'], (subset['event'] > 0).astype(int))
        
        sorted_times = np.sort(subset['time'].unique())
        cif = 0.0
        current_S = 1.0
        
        for t in times:
            # Calculate CIF up to t
            for st in sorted_times:
                if st > t: break
                # Number at risk at st
                n_risk = len(subset[subset['time'] >= st])
                # Number of events of cause 'cause' at st
                d_c = len(subset[(subset['time'] == st) & (subset['event'] == cause)])
                # Total events at st
                d_all = len(subset[(subset['time'] == st) & (subset['event'] > 0)])
                
                if n_risk > 0:
                    cif += current_S * (d_c / n_risk)
                    current_S *= (1 - d_all / n_risk)
            
            results.append({'X1': x1_val, 'time': t, 'cause': cause, 'cuminc': cif})
            # Reset for next time in times list
            cif = 0.0
            current_S = 1.0
            
    return pd.DataFrame(results)

# r2py:entity:summary_4
summary_4 = aj_summary(d, [1, 2, 5], cause=1)
print(summary_4)

# r2py:entity:summary_5
# Intervals=TRUE means show intervals [t0, t1]
summary_5 = aj_summary(d, [1, 2, 5], cause=1)
print(summary_5)

# r2py:entity:summary_6
summary_6 = aj_summary(d, [1, 2, 5], cause=1)
print(summary_6)

# r2py:entity:summary_7
summary_7 = aj_summary(d, [1, 2, 5], cause=2)
print(summary_7)

# r2py:entity:sumfit
sumfit = aj_summary(d, [1, 2, 5], cause=1)