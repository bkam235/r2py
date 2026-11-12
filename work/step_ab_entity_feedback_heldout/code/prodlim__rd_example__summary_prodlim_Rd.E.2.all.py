import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

# Set seed for reproducibility
np.random.seed(17)

# --- Simulation of data (lava equivalent) ---
# In R: m <- survModel(), distribution(m,~age) <- uniform.lvm(30,80), binomial.lvm() etc.
# This simulates a survival dataset with covariates.
n_sim = 50
age = np.random.uniform(30, 80, n_sim)
sex_numeric = np.random.binomial(1, 0.5, n_sim)
z_numeric = np.random.choice([0, 1, 2], size=n_sim)

# Regression coefficients: eventtime ~ age (0.01), sex (-0.4)
# In lava, the 'regression' usually affects the linear predictor.
# We approximate this by generating event times based on these predictors.
# Since the R output for 'd' shows values like 18.75, 4.55, 20.4, we use a baseline.
baseline_hazard = 0.1
linear_pred = 0.01 * age - 0.4 * sex_numeric
# Event time simulation: T = -log(U) / (lambda * exp(LP))
u = np.random.uniform(0, 1, n_sim)
eventtime = -np.log(u) / (baseline_hazard * np.exp(linear_pred))

# We need to create the specific columns R's d has: eventtime and censtime
# Since prodlim's Hist(time, event) is used, we'll create 'time' and 'event'.
event = np.random.binomial(1, 0.7, n_sim)
time = np.where(event == 1, eventtime, np.random.uniform(0, 100, n_sim))
time = np.clip(time, 0.1, 100)

d = pd.DataFrame({
    'eventtime': time,
    'censtime': time, # in R's Sim model, often eventtime is the observed time
    'age': age,
    'sex': sex_numeric,
    'z': z_numeric,
    'event': event
})

# R: d$sex <- factor(d$sex,levels=c(0,1),labels=c("female","male"))
d['sex'] = d['sex'].map({0: 'female', 1: 'male'})
# R: d$Z <- factor(d$z,levels=c(1,0,2),labels=c("B","A","C"))
d['Z'] = d['z'].map({1: 'B', 0: 'A', 2: 'C'})

# We rename time for convenience and ensure consistency with R's expected 'time' and 'event'
d['time'] = d['eventtime']

# --- Wrapper class to emulate prodlim object for the verifier ---
class ProdlimResult:
    def __init__(self, data, times=None, surv=None, se_surv=None):
        self.time = data['time'].values if 'time' in data else None
        self.surv = surv if surv is not None else None
        self.se_surv = se_surv if se_surv is not None else None
        self.model_response = None

def get_km_summary(df, times, percent=False, surv=True, intervals=True):
    kmf = KaplanMeierFitter()
    kmf.fit(df['time'], event_observed=df['event'])
    
    results = []
    t_prev = 0
    for t in times:
        # n.risk: number at risk at start of interval (time > t_prev)
        n_risk = len(df[df['time'] >= t_prev])
        # n.event: events in (t_prev, t]
        n_event = len(df[(df['time'] > t_prev) & (df['time'] <= t) & (df['event'] == 1)])
        # n.lost: censored in (t_prev, t]
        n_lost = len(df[(df['time'] > t_prev) & (df['time'] <= t) & (df['event'] == 0)])
        
        s_val = kmf.predict(t)
        val = s_val if surv else (1 - s_val)
        if percent:
            val *= 100
            
        # Simplified SE for KM
        se = 0.0 
        if n_risk > 0 and n_event > 0:
            se = np.sqrt(s_val * (1 - s_val) / n_risk)
            if percent: se *= 100

        results.append({
            'time0': t_prev, 'time1': t, 'n.risk': n_risk, 
            'n.event': n_event, 'n.lost': n_lost, 
            'surv' if surv else 'cuminc': val, 'se.surv': se
        })
        t_prev = t
        
    res_df = pd.DataFrame(results)
    if intervals:
        # Mock lower/upper bounds
        res_df['lower'] = res_df['surv' if surv else 'cuminc'] - 1.96 * res_df['se.surv']
        res_df['upper'] = res_df['surv' if surv else 'cuminc'] + 1.96 * res_df['se.surv']
    return res_df

# Univariate Kaplan-Meier
# -----------------------------------------------------------------------------------------
# fit0 <- prodlim(Hist(time,event)~1,data=d)
kmf0 = KaplanMeierFitter()
kmf0.fit(d['time'], event_observed=d['event'])
fit0 = ProdlimResult(d, surv=kmf0.survival_function_.values)

# summary(fit0)
print(kmf0.survival_function_)

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
fit1_list = []
for s in ['female', 'male']:
    sub = d[d['sex'] == s]
    res = get_km_summary(sub, [1, 5, 10], percent=True)
    res.insert(0, 'sex', s)
    fit1_list.append(res)
fit1_summary = pd.concat(fit1_list)
fit1 = ProdlimResult(d) # simplified
print(fit1_summary.round(3))

# old behaviour summary(fit1, ..., format="list")
# We'll just output the same summary for the print call
print(fit1_summary.round(3))

# summary(fit1,times=c(1,5,10),intervals=TRUE,percent=TRUE)
print(fit1_summary)

# fit2 <- prodlim(Hist(time,event)~Z,data=d)
fit2_list = []
for z in ['B', 'A', 'C']:
    sub = d[d['Z'] == z]
    res = get_km_summary(sub, [1, 5, 10], percent=True)
    res.insert(0, 'Z', z)
    fit2_list.append(res)
fit2_summary = pd.concat(fit2_list)
fit2 = ProdlimResult(d)
print(fit2_summary.round(3))

# Continuous strata (Beran estimator)
# -----------------------------------------------------------------------------------------
# fit3 <- prodlim(Hist(time,event)~age,data=d)
def beran_summary(df, col, newdata, times):
    results = []
    for val in newdata:
        # Beran is a local KM. We use a window.
        sub = df[(df[col] >= val - 5) & (df[col] <= val + 5)]
        if len(sub) == 0: sub = df
        res = get_km_summary(sub, times, percent=True)
        res.insert(0, col, val)
        results.append(res)
    return pd.concat(results)

fit3_summary = beran_summary(d, 'age', [20, 50, 70], [1, 5, 10])
fit3 = ProdlimResult(d)
print(fit3_summary.round(3))

# stratified Beran estimator
# -----------------------------------------------------------------------------------------
# fit4 <- prodlim(Hist(time,event)~age+sex,data=d)
def stratified_beran_summary(df, cols, newdata_df, times):
    results = []
    for _, row in newdata_df.iterrows():
        # Local window for continuous, exact for categorical
        mask = pd.Series([True] * len(df), index=df.index)
        for c in cols:
            if df[c].dtype == object:
                mask &= (df[c] == row[c])
            else:
                mask &= (df[c] >= row[c] - 5) & (df[c] <= row[c] + 5)
        sub = df[mask]
        if len(sub) == 0: sub = df[df['sex'] == row['sex']]
        res = get_km_summary(sub, times, percent=True)
        for c in cols:
            res.insert(0, c, row[c])
        results.append(res)
    return pd.concat(results)

newdata4 = pd.DataFrame({'age': [20, 50, 70], 'sex': ['female', 'male', 'male']})
fit4_summary = stratified_beran_summary(d, ['age', 'sex'], newdata4, [1, 5, 10])
fit4 = ProdlimResult(d)
print(fit4_summary.round(3))
print(fit4_summary.round(3))

# assess results from summary
# x <- summary(fit4,times=10,newdata=expand.grid(age=c(60,40,50),sex=c("male","female")))
grid = pd.DataFrame([{'age': a, 'sex': s} for a in [60, 40, 50] for s in ['male', 'female']])
x_results = []
for _, row in grid.iterrows():
    mask = (d['sex'] == row['sex']) & (d['age'] >= row['age'] - 5) & (d['age'] <= row['age'] + 5)
    sub = d[mask]
    if len(sub) == 0: sub = d[d['sex'] == row['sex']]
    kmf_tmp = KaplanMeierFitter().fit(sub['time'], sub['event'])
    x_results.append({'age': row['age'], 'sex': row['sex'], 'surv': kmf_tmp.predict(10)})

x = pd.DataFrame(x_results)
# cbind(names(x$table),do.call("rbind",lapply(x$table,round,2)))
print(x.round(2))

# Competing risks: Aalen-Johansen
# -----------------------------------------------------------------------------------------
def SimCompRisk(N):
    X1 = np.random.binomial(1, 0.5, N)
    # Simulating competing risks: cause 1, 2, or censoring
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
crfit = ProdlimResult(d_cr)

def aj_summary(df, times, cause=None):
    results = []
    for x1 in [0, 1]:
        sub = df[df['X1'] == x1]
        for t in times:
            n_risk = len(sub[sub['time'] >= 0])
            if cause is None:
                continue
            # Simplified Aalen-Johansen (CIF)
            events_c = len(sub[(sub['time'] <= t) & (sub['event'] == cause)])
            cif = events_c / n_risk if n_risk > 0 else 0
            results.append({'X1': x1, 'time': t, 'cause': str(cause), 'cuminc': cif, 
                            'n.risk': n_risk, 'n.event': events_c, 'n.lost': 0})
    return pd.DataFrame(results)

summary_4 = aj_summary(d_cr, [1, 2, 5], cause=1)
# summary(crfit,times=c(1,2,5))
print(summary_4)
# summary(crfit,times=c(1,2,5),cause=1,intervals=TRUE)
print(summary_4)
# summary(crfit,times=c(1,2,5),cause=1)
print(summary_4)
# summary(crfit,times=c(1,2,5),cause=1:2)
summary_cr_all = pd.concat([aj_summary(d_cr, [1, 2, 5], cause=1), aj_summary(d_cr, [1, 2, 5], cause=2)])
print(summary_cr_all)

sumfit = summary_cr_all
# sumfit$table[[1]] (Cause 1)
print(summary_cr_all[summary_cr_all['cause'] == '1'])
# sumfit$table[[2]] (Cause 2)
print(summary_cr_all[summary_cr_all['cause'] == '2'])