#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 11:32:12 2026

@author: hiro
"""

import os

import os
os.getcwd()



from pathlib import Path
data_dir = Path("/Users/hiro/Documents/github/Wooldridge/data")
import pandas as pd

# Folder where your .dta files are stored
#data_dir = Path("data")

# Load all .dta files into a dict: {"mroz": df, "wagepan": df, ...}
datasets = {
    f.stem: pd.read_stata(f)
    for f in data_dir.glob("*.dta")
}

print(datasets.keys())         # all dataset names
print(datasets["mroz"].head()) # access dataset by name

from pathlib import Path
import pandas as pd

data_dir = Path("data")

for f in data_dir.glob("*.dta"):
    globals()[f.stem] = pd.read_stata(f)

# Example
print(mroz.head())
print(wagepan.head())


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

if "mroz" in datasets:
    print(datasets["mroz"].head())

if errors:
    print("\nErrors:")
    for k, v in errors.items():
        print(k, "->", v)
        


for name, df in datasets.items():
    globals()[name] = df

print(mroz.head())
print(wagepan.head())