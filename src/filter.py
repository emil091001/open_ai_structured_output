
import json
import os
from config import *
from metrics2 import Metrics
from structure import Structure
import copy
from tqdm import tqdm

from utils.float_conversion import convert_to_float

class Filter:
    tables = [
        'environmental_impact',
        'additional_environmental_impact',
        'resource_use',
        'end_of_life_waste',
        'end_of_life_flow']
    
    def __init__(self, min_param_count=2):
        self.min_param_count = min_param_count
        

    def __call__(self, output: Structure) -> Structure:
        filtered_output = copy.deepcopy(output)
        hashes = set()
        for table in self.tables:
            parameters = getattr(filtered_output, table)
            filtered_parameters = []
            all_zero_count = 0
            for parameter in parameters:
                value_hash = hash(str(parameter.values))
                
                if self.all_values_zero(parameter.values):
                    all_zero_count += 1

                
                if value_hash in hashes and not self.all_values_zero(parameter.values):
                    #print(f"Removing duplicate parameter: {parameter.parameter}")
                    pass#continue
                
                filtered_parameters.append(parameter)
                hashes.add(value_hash)
            
            #print(table, len(filtered_parameters), all_zero_count)
            if len(filtered_parameters) >= self.min_param_count and all_zero_count != len(parameters):
                setattr(filtered_output, table, filtered_parameters)
            else:
                print("")
                print(f"Clearing table: {table}")
                print(output.product_name)
                print(len(parameters), len(filtered_parameters), all_zero_count)
                setattr(filtered_output, table, [])
                
        return filtered_output
    
    def all_values_zero(self, values):
        for value in values:
            float_value = convert_to_float(value.value)
            if float_value != 0:
                return False
        return True


# # output = Structure.parse_file('data/test_output copy.json')
# # target = Structure.parse_file('data/test_target.json')
# output = Structure.parse_file('data/output/Schiebeläden aus Holz.json')
# target = Structure.parse_file('data/target/Schiebeläden aus Holz.json')

# metrics = Metrics()
# #metrics_raw = metrics.calculate(target, output)
# metrics_raw = metrics.calculate_average(target, output)

# filter = Filter()
# filtered_output = filter(output)
# #metrics_filtered = metrics.calculate(target, filtered_output)
# metrics_filtered = metrics.calculate_average(target, filtered_output)


# #print(json.dumps(filtered_output.model_dump(), indent=4))
# #print(json.dumps(metrics_raw, indent=4))
# #print(filtered_averages)
# print(json.dumps(metrics_filtered, indent=4))

# with open('data/filtered_output/Schiebeläden aus Holz.json', 'w') as f:
#     json.dump(filtered_output.model_dump(), f, indent=4)

filter = Filter(min_param_count=0)

not_eq = 0
eq = 0
for target_name in tqdm(os.listdir(TARGET_PATH)[:100]):
    target_path = os.path.join(TARGET_PATH, target_name)    
    target = Structure.parse_file(target_path)
    

    filtered_target = filter(target)
  
    
    if not filtered_target == target:
        not_eq += 1
        continue
    eq += 1
    
        

print(not_eq / (not_eq + eq))
    
    
    