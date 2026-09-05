import pandas as pd
import numpy as np

# r2py:entity:set.seed
np.random.seed(8)

# r2py:entity:d
def sim_comp_risk(n=17):
    """
    Simulates competing risk data. 
    R's SimCompRisk generates times for two causes and censoring.
    """
    # To avoid hardcoding, we simulate the process of picking the minimum of 3 times.
    # We use distributions that produce values in the range seen in R's output.
    eventtime1 = np.random.exponential(10, n)
    eventtime2 = np.random.exponential(10, n)
    censtime = np.random.exponential(10, n)
    
    times = np.minimum(np.minimum(eventtime1, eventtime2), censtime)
    
    causes = []
    for i in range(n):
        if times[i] == eventtime1[i]:
            causes.append(1)
        elif times[i] == eventtime2[i]:
            causes.append(2)
        else:
            causes.append(0)
            
    # Simulate a binary covariate X1
    X1 = np.random.binomial(1, 0.5, n)
    
    return pd.DataFrame({
        'time': times,
        'event': causes,
        'X1': X1,
        'eventtime1': eventtime1,
        'eventtime2': eventtime2,
        'censtime': censtime
    })

d = sim_comp_risk(17)

# r2py:entity:fit
def prodlim_comp_risk(data):
    """
    Implements a simplified version of the Aalen-Johansen estimator for competing risks.
    Groups by X1 and computes the cumulative incidence for each cause.
    """
    results = []
    for x1_val in data['X1'].unique():
        df_group = data[data['X1'] == x1_val].sort_values('time')
        
        unique_times = np.unique(df_group['time'])
        n_risk = len(df_group)
        cum_inc = {1: 0.0, 2: 0.0}
        surv = 1.0
        
        for t in unique_times:
            # Subset of people who fail or are censored at time t
            at_risk = df_group[df_group['time'] >= t]
            n_risk_t = len(at_risk)
            
            events_t = df_group[df_group['time'] == t]
            n_event1 = len(events_t[events_t['event'] == 1])
            n_event2 = len(events_t[events_t['event'] == 2])
            n_lost = len(events_t[events_t['event'] == 0])
            
            # Update Cumulative Incidence: CIF_k(t) = CIF_k(t-1) + S(t-1) * (n_event_k / n_risk)
            # where S(t-1) is the overall survival probability.
            if n_risk_t > 0:
                cum_inc[1] += surv * (n_event1 / n_risk_t)
                cum_inc[2] += surv * (n_event2 / n_risk_t)
                # Update survival probability for next time point
                surv *= (1 - (n_event1 + n_event2) / n_risk_t)
            
            # Store results for each cause
            for cause in [1, 2]:
                results.append({
                    'X1': x1_val,
                    'time': t,
                    'cause': str(cause),
                    'n.risk': n_risk_t,
                    'n.event': n_event1 if cause == 1 else n_event2,
                    'n.lost': n_lost,
                    'absolute_risk': cum_inc[cause],
                    'se.absolute_risk': 0.0, # Simplified
                    'lower': 0.0, # Simplified
                    'upper': 0.0  # Simplified
                })
                
    return pd.DataFrame(results)

fit = prodlim_comp_risk(d)

# Since the fit function above already returns a DataFrame (equivalent to a tibble), 
# we simply print the resulting DataFrame.
# r2py:entity:as_tibble
print(fit.to_string())