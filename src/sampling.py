from collections import defaultdict
import cvxpy as cp
import numpy as np
import pandas as pd
from tqdm import tqdm
import json
import os


modules = ["A1",	"A2",	"A3",	"A1-A3", "A4",	"A5",	"B1",	"B2",	"B3",	"B4",	"B5",	"B6",	"B7",	"C1",	"C2",	"C3",	"C4",	"D"]

parameters = ['GWP-total', 'GWP-fossil', 'GWP-biogenic', 'GWP-luluc', 'ODP', 'AP',
       'ADPE', 'ADPF', 'WDP', 'EP-freshwater', 'EP-marine', 'EP-terrestrial',
       'PM', 'ETP-fw', 'HTP-c', 'HTP-nc', 'SQP', 'IRP', 'PERM', 'PENRM',
       'PENRT', 'SM', 'RSF', 'NRSF', 'HWD', 'RWD', 'CRU', 'MFR', 'MER', 'EEE',
       'EET', 'POCP', 'GWP-IOBC', 'PERE', 'PERT', 'PENRE', 'FW', 'NHWD', 'EP']


tables = [
        'environmental_impact',
        'additional_environmental_impact',
        'resource_use',
        'end_of_life_waste',
        'end_of_life_flow']



epd_list = []
df = pd.DataFrame(index=parameters, columns=modules).fillna(0).astype(int)

lines = []

with open("data/dataset/train4000_2025-04-15.jsonl", 'r', encoding='utf-8') as file:
    for line in tqdm(file):
        lines.append(line)
        data = json.loads(line)
        target = json.loads(data["messages"][2]["content"])
        df[:] = 0
        
        
        for table in tables:
            for parameter_object in target.get(table, []):
                parameter_name = parameter_object['parameter']
                for value_object in parameter_object['values']:
                    module_name = value_object['module']
                    df.loc[parameter_name, module_name] += 1
                               
        df = df[modules]
        df = df.loc[parameters]
        epd_list.append(df.values.flatten())
        
        
A = np.array(epd_list).T

print(A)
print(np.sum(A[0]))


n = A.shape[1]
target_amount = n * 0.5
b = np.ones(A.shape[0]) * target_amount


upper_bound = 16
lam = 10
gamma = 10

# Variable
x = cp.Variable(n)  # non-negative constraint

# Constraints
constraints = [x >= 0, x <= upper_bound]

# Objective
objective = cp.Minimize(cp.sum_squares(A @ x - b) + lam * cp.sum_squares(x) + gamma * (cp.sum(x) -  2 * target_amount) ** 2)

# Problem
problem = cp.Problem(objective, constraints)

# Solve using SCS (uses FISTA-like algorithm under the hood)
problem.solve(solver=cp.SCS, verbose=True, max_iters=2000)  # or try solver=cp.OSQP

x = x.value

print(x)


with open('data/dataset/train4000_2025-04-15_sampled.jsonl', 'w', encoding='utf-8') as outfile:
    for i, line in tqdm(enumerate(lines)):
        for _ in range(round(x[i])):
            outfile.write(line)
    


    