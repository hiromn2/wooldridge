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


X = mroz[['exper',
          'expersq',
          'educ',
          'age',
          'kidslt6',
          'kidsge6']].copy().reset_index(drop=True)

y = mroz['lwage']



#1. Drop NAs and do the simplest analysis




#1.1. OLS
import statsmodels.api as sm
import numpy as np





X = sm.add_constant(X)  # adds the intercept explicitly
model = sm.OLS(y, X).fit()
print(model.summary())



#1.2. Heteroskedasticity robust!

model_hc3  = sm.OLS(y,x).fit(cov_type='HC3')
print(model_hc3.summary())

#2. Instrumental Variables
print("FIRST STAGE — instrument relevance:")
fs_X = sm.add_constant(df[Z_cols + X_cols])
fs   = sm.OLS(df[T_col], fs_X).fit()
fs_fstat = fs.fvalue
print(f"  F-statistic on instruments: {fs_fstat:.2f}  "
      f"({'STRONG (>10)' if fs_fstat > 10 else 'WEAK'})")
print(f"  fatheduc coef: {fs.params['fatheduc']:.4f}  p={fs.pvalues['fatheduc']:.4f}")
print(f"  motheduc coef: {fs.params['motheduc']:.4f}  p={fs.pvalues['motheduc']:.4f}\n")





########################################################################################################################################################################################
# ML Way


