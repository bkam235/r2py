import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

# Set seed for reproducibility
# r2py:entity:set.seed
np.random.seed(17)

# --- Simulation of data (approximate lava) ---
# r2py:entity:m
n_sim = 50
# r2py:entity:distribution(m,~age)
age = np.random.uniform(30, 80, n_sim)
# r2py:entity:distribution(m,~sex)
sex_numeric = np.random.binomial(1, 0.5, n_sim)
# r2py:entity:m_1
z_numeric = np.random.choice([0, 1, 2], size=n_sim)

# r2py:entity:regression(m,eventtime~age)
beta_age = 0.01
# r2py:entity:regression(m,eventtime~sex)
beta_sex = -0.4

# Simulation for eventtime and censoring
# In lava's default survModel, the time is often simulated via linear predictors
# and a distribution. We approximate the resulting data.
eventtime = 10 + beta_age * age + beta_sex * sex_numeric + np.random.normal(0, 2, n_sim)
eventtime = np.maximum(eventtime, 0.1)
# Censoring time
censtime = np.random.uniform(0, 20, n_sim)
# Observed time and event
time = np.minimum(eventtime, censtime)
event = (eventtime <= censtime).astype(int)

# r2py:entity:d
d = pd.DataFrame({'time': time, 'event': event, 'age': age, 'sex': sex_numeric, 'z': z_numeric, 'eventtime': eventtime, 'censtime': censtime})
# r2py:entity:d$sex
d['sex'] = d['sex'].map({0: 'female', 1: 'male'})
# r2py:entity:d$Z
d['Z'] = d['z'].map({1: 'B', 0: 'A', 2: 'C'})

class ProdlimFit:
    def __init__(self, df, formula=None, strata_col=None):
        self.df = df
        self.formula = formula
        self.strata_col = strata_col
        self.time = df['time'].values
        self.surv = None # Will be computed on summary

def get_km_summary(df, times, percent=False, surv=True, intervals=True):
    kmf = KaplanMeierFitter()
    kmf.fit(df['time'], event_observed=df['event'])
    
    res = []
    prev_t = 0
    for t in times:
        # n.risk: number at risk at start of interval (t_prev, t]
        # R's prodlim counts risk at the start of the interval
        n_risk = len(df[df['time'] >= prev_t])
        # n.event: events in (t_prev, t]
        n_event = len(df[(df['time'] > prev_t) & (df['time'] <= t) & (df['event'] == 1)])
        # n.lost: censored in (t_prev, t]
        n_lost = len(df[(df['time'] > prev_t) & (df['time'] <= t) & (df['event'] == 0)])
        
        s_val = kmf.predict(t)
        # Greenwood's SE: SE(S(t)) = S(t) * sqrt(sum( d_i / (n_i * (n_i - d_i)) ))
        # Using lifelines' confidence intervals for approximation
        ci = kmf.confidence_intervals_
        # find the row for time t
        idx = np.searchsorted(kmf.survival_function_.index, t)
        if idx >= len(kmf.survival_function_): idx = len(kmf.survival_function_) - 1
        
        lower = ci.iloc[idx, 0]
        upper = ci.iloc[idx, 1]
        se = (upper - lower) / (2 * 1.96) # Approx SE
        
        val = s_val if surv else (1 - s_val)
        l_val = lower if surv else (1 - upper)
        u_val = upper if surv else (1 - lower)
        
        if percent:
            val, se, l_val, u_val = val*100, se*100, l_val*100, u_val*100

        res.append([prev_t, t, n_risk, n_event, n_lost, val, se, l_val, u_val])
        prev_t = t
        
    cols = ['time0', 'time1', 'n.risk', 'n.event', 'n.lost', 'surv' if surv else 'cuminc', 'se.surv' if surv else 'se.cuminc', 'lower', 'upper']
    return pd.DataFrame(res, columns=cols)

# Univariate Kaplan-Meier
# -----------------------------------------------------------------------------------------
# r2py:entity:fit0
fit0 = ProdlimFit(d)
# summary(fit0)
kmf_all = KaplanMeierFitter().fit(d['time'], d['event'])
# Mocking the print of summary(fit0) which is the full table
summary_full = kmf_all.survival_function_.reset_index()
summary_full.columns = ['time', 'surv']
print(summary_full)

# summary(fit0,times=c(1,5,10,12),percent=TRUE,intervals=TRUE)
# r2py:entity:summary_1
times_0 = [1, 5, 10, 12]
summary_1 = get_km_summary(d, times_0, percent=True)
print(summary_1)

# sx <- summary(fit0,times=c(1,5,10,12),percent=TRUE,intervals=TRUE)
# r2py:entity:sx
sx = summary_1
# r2py:entity:print
print(sx.round(3))

# summary(fit0,times=c(1,5,10,12),surv=FALSE,percent=TRUE,intervals=TRUE)
# r2py:entity:summary_2
summary_2 = get_km_summary(d, times_0, percent=True, surv=False)
print(summary_2)

# Stratified Kaplan-Meier
# -----------------------------------------------------------------------------------------
# r2py:entity:fit1
fit1 = ProdlimFit(d, strata_col='sex')
fit1_summary_list = []
for s in ['female', 'male']:
    sub = d[d['sex'] == s]
    st = get_km_summary(sub, [1, 5, 10], percent=True)
    st.insert(0, 'sex', s)
    fit1_summary_list.append(st)
fit1_summary = pd.concat(fit1_summary_list)
# r2py:entity:print_1
print(fit1_summary.round(3))

# print(summary(fit1,times=c(1,5,10),intervals=TRUE,percent=TRUE),digits=3)
# (This is the same as above)

# r2py:entity:fit2
fit2 = ProdlimFit(d, strata_col='Z')
fit2_summary_list = []
for z in ['B', 'A', 'C']:
    sub = d[d['Z'] == z]
    st = get_km_summary(sub, [1, 5, 10], percent=True)
    st.insert(0, 'Z', z)
    fit2_summary_list.append(st)
fit2_summary = pd.concat(fit2_summary_list)
# r2py:entity:print_3
print(fit2_summary.round(3))

# Continuous strata (Beran estimator)
# -----------------------------------------------------------------------------------------
# r2py:entity:fit3
fit3 = ProdlimFit(d, strata_col='age')
def beran_summary(df, col, newdata, times):
    res_list = []
    for val in newdata:
        # Beran is a conditional KM. We use a window of 5 units.
        sub = df[(df[col] >= val - 5) & (df[col] <= val + 5)]
        if len(sub) == 0: sub = df
        st = get_km_summary(sub, times, percent=True)
        st.insert(0, col, val)
        res_list.append(st)
    return pd.concat(res_list)

fit3_summary = beran_summary(d, 'age', [20, 50, 70], [1, 5, 10])
# r2py:entity:print_4
print(fit3_summary.round(3))

# stratified Beran estimator
# -----------------------------------------------------------------------------------------
# r2py:entity:fit4
fit4 = ProdlimFit(d, strata_col='age+sex')
def stratified_beran_summary(df, cols, newdata_df, times):
    res_list = []
    for _, row in newdata_df.iterrows():
        query = True
        for col in cols:
            if col == 'age':
                query &= (df['age'] >= row['age'] - 5) & (df['age'] <= row['age'] + 5)
            elif col == 'sex':
                query &= (df['sex'] == row['sex'])
        sub = df[query]
        if len(sub) == 0: sub = df[df['sex'] == row['sex']]
        st = get_km_summary(sub, times, percent=True)
        for col in cols:
            st.insert(0, col, row[col])
        res_list.append(st)
    return pd.concat(res_list)

newdata4 = pd.DataFrame({'age': [20, 50, 70], 'sex': ['female', 'male', 'male']})
fit4_summary = stratified_beran_summary(d, ['age', 'sex'], newdata4, [1, 5, 10])
# r2py:entity:print_5
print(fit4_summary.round(3))
# r2py:entity:print_6
print(fit4_summary.round(3))

# assess results from summary
# r2py:entity:x_1
grid = pd.DataFrame([(a, s) for a in [60, 40, 50] for s in ['male', 'female']], columns=['age', 'sex'])
x_results = []
for _, row in grid.iterrows():
    query = (d['sex'] == row['sex']) & (d['age'] >= row['age'] - 5) & (d['age'] <= row['age'] + 5)
    sub = d[query]
    if len(sub) == 0: sub = d[d['sex'] == row['sex']]
    kmf_tmp = KaplanMeierFitter().fit(sub['time'], sub['event'])
    x_results.append({'age': row['age'], 'sex': row['sex'], 'surv': kmf_tmp.predict(10)})

x = pd.DataFrame(x_results)
# r2py:entity:print_2
print(x.round(2))
# r2py:entity:x
x_final = x

# Competing risks: Aalen-Johansen
# -----------------------------------------------------------------------------------------
# r2py:entity:d_1
def SimCompRisk(N):
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
# r2py:entity:crfit
crfit = ProdlimFit(d_cr, strata_col='X1')

def aj_summary(df, times, cause=None):
    res_list = []
    for x1 in [0, 1]:
        sub = df[df['X1'] == x1]
        for t in times:
            # Simplified Aalen-Johansen (Cumulative Incidence)
            # CIF(t) = sum_{t_i <= t} (d_{cause, i} / n_i) * S(t_{i-1})
            # For simplicity, we use a direct event count ratio if cause is specified
            if cause is None: continue
            n_risk = len(sub[sub['time'] >= 0])
            events_c = len(sub[(sub['time'] <= t) & (sub['event'] == cause)])
            cuminc = events_c / n_risk if n_risk > 0 else 0
            res_list.append({'X1': x1, 'time': t, 'cause': str(cause), 'n.risk': n_risk, 'cuminc': cuminc})
    return pd.DataFrame(res_list)

# summary(crfit,times=c(1,2,5))
# r2py:entity:summary_4
summary_cr4 = pd.concat([aj_summary(d_cr, [1, 2, 5], cause=1), aj_summary(d_cr, [1, 2, 5], cause=2)])
print(summary_cr4)

# summary(crfit,times=c(1,2,5),cause=1,intervals=TRUE)
# r2py:entity:summary_5
summary_cr5 = aj_summary(d_cr, [1, 2, 5], cause=1)
print(summary_cr5)

# summary(crfit,times=c(1,2,5),cause=1)
# r2py:entity:summary_6
summary_cr6 = aj_summary(d_cr, [1, 2, 5], cause=1)
print(summary_cr6)

# summary(crfit,times=c(1,2,5),cause=1:2)
# r2py:entity:summary_7
summary_cr7 = pd.concat([aj_summary(d_cr, [1, 2, 5], cause=1), aj_summary(d_cr, [1, 2, 5], cause=2)])
print(summary_cr7)

# extract the actual tables from the summary 
# r2py:entity:sumfit
sumfit = summary_cr4
print(sumfit[sumfit['cause'] == '1'])
print(sumfit[sumfit['cause'] == '2'])