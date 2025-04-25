import os
import json
from config import *
from structure import Structure
from tqdm import tqdm
import pandas as pd


df = pd.DataFrame()

tables = [
        'environmental_impact',
        'additional_environmental_impact',
        'resource_use',
        'end_of_life_waste',
        'end_of_life_flow']

for file_name in tqdm(os.listdir(TARGET_PATH)):
    target = Structure.parse_file(os.path.join(TARGET_PATH, file_name))
    
    for table in tables:
        parameters = getattr(target, table)
        for parameter in parameters:
            df[parameter.parameter] 


