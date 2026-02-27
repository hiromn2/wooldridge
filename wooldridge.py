#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 11:32:12 2026

@author: hiro
"""

from pathlib import Path
import pyreadstat

data_dir = Path("/Users/hiro/Documents/github/Wooldridge/data")

datasets = {}
errors = {}

for f in data_dir.glob("*.dta"):
    try:
        df, meta = pyreadstat.read_dta(str(f))
        datasets[f.stem] = df
    except Exception as e:
        errors[f.name] = str(e)

print("Loaded:", len(datasets))
print("Some names:", list(datasets.keys())[:10])


for name, df in datasets.items():
    globals()[name] = df


########################################################################################################################################################################################
# Statistical/Econometric Way

#0. Setup


df = mroz[mroz['inlf'] == 1].copy().reset_index(drop=True)
X = df[['exper',
          'expersq',
          'educ',
          'age',
          'kidslt6',
          'kidsge6']].copy().reset_index(drop=True)

y = df['lwage']

Y_col  = 'lwage'          # outcome: log(wage)
T_col  = 'educ'           # treatment: years of education
Z_cols = ['fatheduc',
          'motheduc']     # instruments: parents' education
X_cols = ['exper',
          'expersq',
          'age',
          'kidslt6',
          'kidsge6']      # controls


#1. Drop NAs and do the simplest analysis




#1.1. OLS
import statsmodels.api as sm
import numpy as np





X = sm.add_constant(X)  # adds the intercept explicitly
model = sm.OLS(y, X).fit()
print(model.summary())



#1.2. Heteroskedasticity robust!

model_hc3  = sm.OLS(y,X).fit(cov_type='HC3')
print(model_hc3.summary())

#2. Checking Instrument relevance!!!

# Check if instruments are relevant
fs_X = sm.add_constant(df[Z_cols + X_cols])
fs   = sm.OLS(df[T_col], fs_X).fit()
print(fs.summary())
fs_fstat = fs.fvalue #This is F-statistic
print(f"  F-statistic on instruments: {fs_fstat:.2f}  "
      f"({'STRONG (>10)' if fs_fstat > 10 else 'WEAK'})")

#For custom joint hypotheses
hypotheses = "age = 0, kidslt6 = 0"
f_test = fs.f_test(hypotheses)
print(f_test)



#2.1 2SLS with linearmodels

from linearmodels.iv import IV2SLS

# Formula-based API
iv_formula = (
    f"{Y_col} ~ 1 + {' + '.join(X_cols)}"
    f" [{T_col} ~ {' + '.join(Z_cols)}]"
)
iv_model = IV2SLS.from_formula(iv_formula, data=df).fit(cov_type='robust')

print(iv_model.summary.tables[1]) #2SLS estimate of beta of educ 0.0578 (SE = 0.0337)
# IV gives a lower estimate, consistent with bias pulling OLS upward

hausman = iv_model.wooldridge_regression #endogeneity confirmed! educ is endogenous


# 3. Dowhy
import dowhy
from dowhy import CausalModel

causal_graph = """
digraph {
    educ        -> lwage;
    exper       -> lwage;
    expersq     -> lwage;
    age         -> lwage;
    kidslt6     -> lwage;
    kidsge6     -> lwage;
    fatheduc    -> educ;
    motheduc    -> educ;
    exper       -> educ;
    age         -> educ;
    U [label="Ability (unobserved)"];
    U -> educ;
    U -> lwage;
}
"""

model_dowhy = CausalModel(
    data=df,
    treatment=T_col,
    outcome=Y_col,
    graph=causal_graph,
    instruments=Z_cols
)



########################################################################################################################################################################################
# ML Way


