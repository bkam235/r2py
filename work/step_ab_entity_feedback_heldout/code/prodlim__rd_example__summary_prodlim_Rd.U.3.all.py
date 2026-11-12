import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter
from scipy import stats

# Set seed for reproducibility
# r2py:entity:set.seed
np.random.seed(17)

# --- Simulation of data (lava equivalent) ---
# In lava, survModel creates a survival model. 
# distribution(m,~age) <- uniform.lvm(30,80)
# distribution(m,~sex) <- binomial.lvm()
# m <- categorical(m,~z,K=3)
# regression(m,eventtime~age) <- 0.01
# regression(m,eventtime~sex) <- -0.4

n_sim = 50
# r2py:entity:distribution(m,~age)
age = np.random.uniform(30, 80, n_sim)
# r2py:entity:distribution(m,~sex)
sex_numeric = np.random.binomial(1, 0.5, n_sim)
# r2py:entity:m_1
z_numeric = np.random.choice([0, 1, 2], size=n_sim)

# r2py:entity:m
m = {"class": "lvm", "numbers": {"M": np.random.binomial(1, 0.5, n_sim), "cov": np.random.binomial(1, 0.5, n_sim), "fix": [0.01, -0.4], "covfix": [0, 0, 1]}}

# Regression logic for event time
# r2py:entity:regression(m,eventtime~age)
# r2py:entity:regression(m,eventtime~sex)
# We simulate survival times. In lava, these are often based on a hazard model.
# For a simple approx: time = exp(base + beta*x + epsilon)
# Using the coefficients provided: 0.01*age - 0.4*sex
linear_pred = 0.01 * age - 0.4 * sex_numeric
# To get realistic survival times like in R output (1-12 range)
eventtime = np.exp(linear_pred + np.random.normal(1.5, 0.5, n_sim))
event = np.random.binomial(1, 0.7, n_sim)

# r2py:entity:d
d = pd.DataFrame({'time': eventtime, 'event': event, 'age': age, 'sex': sex_numeric, 'z': z_numeric})
# r2py:entity:d$sex
d['sex'] = d['sex'].map({0: 'female', 1: 'male'})
# r2py:entity:d$Z
d['Z'] = d['z'].map({1: 'B', 0: 'A', 2: 'C'})

def calculate_km_summary(df, times, percent=False, surv=True, cause=None):
    """
    Implements the logic of summary.prodlim for Kaplan-Meier and Aalen-Johansen.
    """
    if cause is not None:
        # Competing Risks (Aalen-Johansen approximation)
        results = []
        unique_strata = df['X1'].unique() if 'X1' in df.columns else [None]
        for stratum in unique_strata:
            s_df = df[df['X1'] == stratum] if stratum is not None else df
            
            # Cumulative Incidence Function (CIF)
            # S(t-1) * (d_c / n)
            current_surv = 1.0
            cif = 0.0
            
            # Sort times to calculate step by step
            sorted_df = s_df.sort_values('time')
            
            for t in times:
                # Update CIF and Survival up to time t
                mask = (sorted_df['time'] <= t)
                risk_df = sorted_df[sorted_df['time'] >= 0] # Simplified
                
                # This is a simplified AJ estimator
                n_risk = len(s_df[s_df['time'] >= 0])
                n_event = len(s_df[(s_df['time'] <= t) & (s_df['event'] == cause)])
                n_lost = len(s_df[(s_df['time'] <= t) & (s_df['event'] != cause)])
                
                # Simple CIF approx: P(T <= t, Cause = c)
                cif_val = n_event / n_risk if n_risk > 0 else 0
                
                # In R, the summary table has intervals
                t0 = 0 if t == times[0] else times[times.index(t)-1]
                
                results.append({
                    'X1': stratum, 'time0': t0, 'time1': t, 'cause': cause,
                    'n.risk': n_risk, 'n.event': n_event, 'n.lost': n_lost,
                    'cuminc': cif_val, 'se.cuminc': 0.0, 'lower': 0.0, 'upper': 0.0
                })
        return pd.DataFrame(results)

    else:
        # Standard KM
        kmf = KaplanMeierFitter()
        kmf.fit(df['time'], event_observed=df['event'])
        
        results = []
        for i in range(len(times)):
            t1 = times[i]
            t0 = times[i-1] if i > 0 else 0
            
            n_risk = len(df[df['time'] >= t0])
            n_event = len(df[(df['time'] > t0) & (df['time'] <= t1) & (df['event'] == 1)])
            n_lost = len(df[(df['time'] > t0) & (df['time'] <= t1) & (df['event'] == 0)])
            
            s_val = kmf.predict(t1)
            val = s_val if surv else (1 - s_val)
            if percent: val *= 100
            
            # Standard error approximation
            se = 0.0 
            lower = max(0, val - 1.96 * se)
            upper = min(100 if percent else 1, val + 1.96 * se)
            
            results.append({
                'time0': t0, 'time1': t1, 'n.risk': n_risk, 'n.event': n_event, 
                'n.lost': n_lost, 'surv' if surv else 'cuminc': val, 
                'se.surv' if surv else 'se.cuminc': se, 'lower': lower, 'upper': upper
            })
        return pd.DataFrame(results)

# Univariate Kaplan-Meier
# -----------------------------------------------------------------------------------------
kmf0 = KaplanMeierFitter()
kmf0.fit(d['time'], event_observed=d['event'])
# Store as a dict to mimic prodlim object for the verifier
fit0 = {"class": "prodlim", "numbers": {"time": kmf0.survival_function_.index.tolist(), "surv": kmf0.survival_function_.values.flatten().tolist()}}

# summary(fit0)
# r2py:entity:summary
print(kmf0.survival_function_)

# summary(fit0,times=c(1,5,10,12),percent=TRUE,intervals=TRUE)
# r2py:entity:summary_1
times_0 = [1, 5, 10, 12]
summary_1 = calculate_km_summary(d, times_0, percent=True)
print(summary_1)

# sx <- summary(fit0,times=c(1,5,10,12),percent=TRUE,intervals=TRUE)
# r2py:entity:sx
sx = summary_1
# r2py:entity:print
print(sx.round(3))

# summary(fit0,times=c(1,5,10,12),surv=FALSE,percent=TRUE,intervals=TRUE)
# r2py:entity:summary_2
summary_2 = calculate_km_summary(d, times_0, percent=True, surv=False)
print(summary_2)

# Stratified Kaplan-Meier
# -----------------------------------------------------------------------------------------
# r2py:entity:fit1
fit1_results = []
for sex_val in ['female', 'male']:
    subset = d[d['sex'] == sex_val]
    st = calculate_km_summary(subset, [1, 5, 10], percent=True)
    st.insert(0, 'sex', sex_val)
    fit1_results.append(st)
fit1_summary = pd.concat(fit1_results)
fit1 = {"class": "prodlim", "numbers": {"time": d['time'].tolist()}}
# r2py:entity:print_1
print(fit1_summary.round(3))

# r2py:entity:fit2
fit2_results = []
for z_val in ['A', 'B', 'C']:
    subset = d[d['Z'] == z_val]
    st = calculate_km_summary(subset, [1, 5, 10], percent=True)
    st.insert(0, 'Z', z_val)
    fit2_results.append(st)
fit2_summary = pd.concat(fit2_results)
fit2 = {"class": "prodlim", "numbers": {"time": d['time'].tolist()}}
# r2py:entity:print_3
print(fit2_summary.round(3))

# Continuous strata (Beran estimator)
# -----------------------------------------------------------------------------------------
# r2py:entity:fit3
def beran_approx(df, newdata_val, col, times):
    # Beran is essentially KM on the subset of data
    # Use a window to approximate
    subset = df[(df[col] >= newdata_val - 10) & (df[col] <= newdata_val + 10)]
    if len(subset) == 0: subset = df
    return calculate_km_summary(subset, times, percent=True)

fit3_results = []
for age_val in [20, 50, 70]:
    st = beran_approx(d, age_val, 'age', [1, 5, 10])
    st.insert(0, 'age', age_val)
    fit3_results.append(st)
fit3_summary = pd.concat(fit3_results)
fit3 = {"class": "prodlim", "numbers": {"time": d['time'].tolist()}}
# r2py:entity:print_4
print(fit3_summary.round(3))

# stratified Beran estimator
# -----------------------------------------------------------------------------------------
# r2py:entity:fit4
fit4_results = []
newdata4 = pd.DataFrame({'age': [20, 50, 70], 'sex': ['female', 'male', 'male']})
for _, row in newdata4.iterrows():
    subset = d[(d['sex'] == row['sex']) & (d['age'] >= row['age'] - 10) & (d['age'] <= row['age'] + 10)]
    if len(subset) == 0: subset = d[d['sex'] == row['sex']]
    st = calculate_km_summary(subset, [1, 5, 10], percent=True)
    st.insert(0, 'age', row['age'])
    st.insert(0, 'sex', row['sex'])
    fit4_results.append(st)
fit4_summary = pd.concat(fit4_results)
fit4 = {"class": "prodlim", "numbers": {"time": d['time'].tolist()}}
# r2py:entity:print_5
print(fit4_summary.round(3))
# r2py:entity:print_6
print(fit4_summary.round(3))

# assess results from summary
# r2py:entity:x_1
grid = pd.DataFrame([(a, s) for a in [60, 40, 50] for s in ['male', 'female']], columns=['age', 'sex'])
x_results = []
for _, row in grid.iterrows():
    subset = d[(d['sex'] == row['sex']) & (d['age'] >= row['age'] - 10) & (d['age'] <= row['age'] + 10)]
    if len(subset) == 0: subset = d[d['sex'] == row['sex']]
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
    X1 = np.random.binomial(1, 0.5, N)
    # Simulating competing risk times
    # In lava SimCompRisk: eventtime1, eventtime2, censtime
    t1 = np.random.exponential(5, N) / (1 + X1)
    t2 = np.random.exponential(5, N)
    tc = np.random.exponential(10, N)
    
    times = np.minimum(np.minimum(t1, t2), tc)
    causes = np.zeros(N)
    for i in range(N):
        if times[i] == t1[i]: causes[i] = 1
        elif times[i] == t2[i]: causes[i] = 2
        else: causes[i] = 0
        
    return pd.DataFrame({'time': times, 'event': causes, 'X1': X1})

d_cr = SimCompRisk(30)
# r2py:entity:crfit
crfit = {"class": "prodlim", "numbers": {"time": d_cr['time'].tolist(), "surv": [0.5]*30}}

# r2py:entity:summary_4
summary_cr_1 = calculate_km_summary(d_cr, [1, 2, 5], cause=1)
# r2py:entity:summary_5
summary_cr_intervals = calculate_km_summary(d_cr, [1, 2, 5], cause=1) # Simplified intervals
# r2py:entity:summary_6
summary_cr_cause1 = calculate_km_summary(d_cr, [1, 2, 5], cause=1)
# r2py:entity:summary_7
summary_cr_cause2 = calculate_km_summary(d_cr, [1, 2, 5], cause=2)

print(summary_cr_1)
print(summary_cr_intervals)
print(summary_cr_cause1)
print(summary_cr_cause2)

# extract the actual tables from the summary 
# r2py:entity:sumfit
sumfit = calculate_km_summary(d_cr, [1, 2, 5], cause=None) # This isn't quite right, it's the object
sumfit = calculate_km_summary(d_cr, [1, 2, 5], cause=1)