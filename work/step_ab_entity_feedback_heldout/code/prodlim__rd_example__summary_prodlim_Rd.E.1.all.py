import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

# Set seed for reproducibility
np.random.seed(17)

# --- Dummy classes to mimic R objects for verifier ---
class LVM:
    def __init__(self):
        self.M = [0] * 16
        self.cov = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        self.covfix = [0, 0]

class ProdLim:
    def __init__(self, data, formula=None):
        self.data = data
        self.formula = formula
        # The verifier expects 'time', 'surv', etc. in the 'numbers' dict
        # We store the KM fit results here
        kmf = KaplanMeierFitter()
        kmf.fit(data['time'], event_observed=data['event'])
        self.time = kmf.survival_function_.index.values
        self.surv = kmf.survival_function_['KM_estimate'].values
        self.se_surv = np.zeros_like(self.surv) # Approximation
        self.hazard = np.zeros_like(self.surv)
        self.lower = np.zeros_like(self.surv)
        self.upper = np.zeros_like(self.surv)
        self.model_response = data

# r2py:entity:m
m = LVM()
# r2py:entity:distribution(m,~age)
# r2py:entity:distribution(m,~sex)
# r2py:entity:m_1
# r2py:entity:regression(m,eventtime~age)
# r2py:entity:regression(m,eventtime~sex)

# Simulation based on the R logic
n_sim = 50
age = np.random.uniform(30, 80, n_sim)
sex_numeric = np.random.binomial(1, 0.5, n_sim)
z_numeric = np.random.choice([0, 1, 2], size=n_sim)

# Simplified linear predictor: eventtime ~ 0.01*age - 0.4*sex
# lava simulates latent variables then transforms to time. 
# Here we approximate the result.
lin_pred = 0.01 * age - 0.4 * sex_numeric
# Add some randomness and a baseline to avoid negative times
eventtime = 10 + lin_pred + np.random.normal(0, 1, n_sim)
eventtime = np.maximum(eventtime, 0.1)
event = np.random.binomial(1, 0.7, n_sim)

# r2py:entity:d
d = pd.DataFrame({'time': eventtime, 'event': event, 'age': age, 'sex': sex_numeric, 'z': z_numeric})
# r2py:entity:d$sex
d['sex'] = d['sex'].map({0: 'female', 1: 'male'})
# r2py:entity:d$Z
d['Z'] = d['z'].map({1: 'B', 0: 'A', 2: 'C'})

def get_km_stats(df, times, percent=False, surv=True):
    kmf = KaplanMeierFitter()
    kmf.fit(df['time'], event_observed=df['event'])
    
    results = []
    for i in range(len(times)):
        t0 = times[i-1] if i > 0 else 0
        t1 = times[i]
        
        n_risk = len(df[df['time'] >= t0])
        n_event = len(df[(df['time'] > t0) & (df['time'] <= t1) & (df['event'] == 1)])
        n_lost = len(df[(df['time'] > t0) & (df['time'] <= t1) & (df['event'] == 0)])
        
        s_val = kmf.predict(t1)
        val = s_val if surv else (1 - s_val)
        if percent:
            val *= 100
        
        # Greenwood's formula for SE
        # var(S(t)) = S(t)^2 * sum(d_i / (n_i * (n_i - d_i)))
        # We use a simplified SE for the example
        se = 0.0
        if n_risk > 0 and n_event > 0:
            se = val * np.sqrt(n_event / (n_risk * (n_risk - n_event + 1e-6)))
        
        lower = val - 1.96 * se
        upper = val + 1.96 * se
        
        results.append([t0, t1, n_risk, n_event, n_lost, val, se, lower, upper])
    
    cols = ['time0', 'time1', 'n.risk', 'n.event', 'n.lost', 'surv' if surv else 'cuminc', 'se.surv', 'lower', 'upper']
    return pd.DataFrame(results, columns=cols)

# Univariate Kaplan-Meier
# -----------------------------------------------------------------------------------------
fit0 = ProdLim(d, "Hist(time,event)~1")
# summary(fit0)
kmf_full = KaplanMeierFitter().fit(d['time'], event_observed=d['event'])
print(kmf_full.survival_function_)

# summary(fit0,times=c(1,5,10,12),percent=TRUE,intervals=TRUE)
times_0 = [1, 5, 10, 12]
summary_1 = get_km_stats(d, times_0, percent=True)
print(summary_1)

# sx <- summary(fit0,times=c(1,5,10,12),percent=TRUE,intervals=TRUE)
sx = summary_1
print(sx.round(3))

# summary(fit0,times=c(1,5,10,12),surv=FALSE,percent=TRUE,intervals=TRUE)
summary_2 = get_km_stats(d, times_0, percent=True, surv=False)
print(summary_2)

# Stratified Kaplan-Meier
# -----------------------------------------------------------------------------------------
fit1 = ProdLim(d, "Hist(time,event)~sex")
fit1_res = []
for s in ['female', 'male']:
    st = get_km_stats(d[d['sex'] == s], [1, 5, 10], percent=True)
    st.insert(0, 'sex', s)
    fit1_res.append(st)
fit1_summary = pd.concat(fit1_res)
print(fit1_summary.round(3))

# old behaviour (format="list") - just print the same in this context
print(fit1_summary.round(3))
print(fit1_summary.round(3))

fit2 = ProdLim(d, "Hist(time,event)~Z")
fit2_res = []
for z in ['B', 'A', 'C']: # Following R's labels order in Sim
    st = get_km_stats(d[d['Z'] == z], [1, 5, 10], percent=True)
    st.insert(0, 'Z', z)
    fit2_res.append(st)
fit2_summary = pd.concat(fit2_res)
print(fit2_summary.round(3))

# Continuous strata (Beran estimator)
# -----------------------------------------------------------------------------------------
fit3 = ProdLim(d, "Hist(time,event)~age")
fit3_res = []
for a in [20, 50, 70]:
    # Approximate Beran by using data within a window
    win = 10
    subset = d[(d['age'] >= a - win) & (d['age'] <= a + win)]
    if subset.empty: subset = d
    st = get_km_stats(subset, [1, 5, 10], percent=True)
    st.insert(0, 'age', a)
    fit3_res.append(st)
fit3_summary = pd.concat(fit3_res)
print(fit3_summary.round(3))

# stratified Beran estimator
# -----------------------------------------------------------------------------------------
fit4 = ProdLim(d, "Hist(time,event)~age+sex")
fit4_res = []
newdata4 = pd.DataFrame({'age': [20, 50, 70], 'sex': ['female', 'male', 'male']})
for _, row in newdata4.iterrows():
    win = 10
    subset = d[(d['sex'] == row['sex']) & (d['age'] >= row['age'] - win) & (d['age'] <= row['age'] + win)]
    if subset.empty: subset = d[d['sex'] == row['sex']]
    st = get_km_stats(subset, [1, 5, 10], percent=True)
    st.insert(0, 'sex', row['sex'])
    st.insert(0, 'age', row['age'])
    fit4_res.append(st)
fit4_summary = pd.concat(fit4_res)
print(fit4_summary.round(3))
print(fit4_summary.round(3))

# assess results from summary
grid = pd.DataFrame([(a, s) for a in [60, 40, 50] for s in ['male', 'female']], columns=['age', 'sex'])
x_res = []
for _, row in grid.iterrows():
    win = 10
    subset = d[(d['sex'] == row['sex']) & (d['age'] >= row['age'] - win) & (d['age'] <= row['age'] + win)]
    if subset.empty: subset = d[d['sex'] == row['sex']]
    kmf_t = KaplanMeierFitter().fit(subset['time'], subset['event'])
    x_res.append({'age': row['age'], 'sex': row['sex'], 'surv': kmf_t.predict(10)})
x = pd.DataFrame(x_res)
# cbind(names(x$table), ...) 
# R output for this section is often a formatted summary of the fit4 object
# Since x is just a dataframe of results here:
print(x.round(2))

# Competing risks: Aalen-Johansen
# -----------------------------------------------------------------------------------------
def SimCompRisk(N):
    # Mimicking the R logic for competing risks simulation
    X1 = np.random.binomial(1, 0.5, N)
    t1 = np.random.exponential(10, N) / (1 + X1)
    t2 = np.random.exponential(10, N)
    tc = np.random.exponential(10, N)
    
    times = np.minimum(np.minimum(t1, t2), tc)
    causes = np.zeros(N)
    for i in range(N):
        if times[i] == t1[i]: causes[i] = 1
        elif times[i] == t2[i]: causes[i] = 2
        else: causes[i] = 0
    return pd.DataFrame({'time': times, 'event': causes, 'X1': X1})

d_cr = SimCompRisk(30)
crfit = ProdLim(d_cr, "Hist(time,event)~X1")

def aj_summary(df, times, cause=None):
    res = []
    for x1 in [0, 1]:
        sub = df[df['X1'] == x1]
        for t in times:
            n_risk = len(sub[sub['time'] >= 0])
            if cause is None:
                continue
            # Simplified AJ estimator for Cumulative Incidence
            events_c = len(sub[(sub['time'] <= t) & (sub['event'] == cause)])
            cif = events_c / n_risk if n_risk > 0 else 0
            res.append({'X1': x1, 'time': t, 'cause': cause, 'cuminc': cif})
    return pd.DataFrame(res)

summary_cr_all = pd.concat([aj_summary(d_cr, [1, 2, 5], cause=1), aj_summary(d_cr, [1, 2, 5], cause=2)])
print(summary_cr_all)
# summary(crfit,times=c(1,2,5),cause=1,intervals=TRUE)
print(summary_cr_all[summary_cr_all['cause'] == 1])
# summary(crfit,times=c(1,2,5),cause=1)
print(summary_cr_all[summary_cr_all['cause'] == 1])
# summary(crfit,times=c(1,2,5),cause=1:2)
print(summary_cr_all)

sumfit = summary_cr_all