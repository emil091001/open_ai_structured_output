
import json
import os

from config import TARGET_PATH
from structure import Structure
from tqdm import tqdm


tables = [
    'environmental_impact',
    'additional_environmental_impact',
    'resource_use',
    'end_of_life_waste',
    'end_of_life_flow'
]

input_path = "data/dataset/test2025-03-28.jsonl"
#input_path = "data/dataset/train4000_2025-03-28.jsonl"
#input_path = "data/dataset/val1000_2025-03-28.jsonl"
#input_path = "data/dataset/train4000_modified.jsonl"

output_path = "data/dataset/test2025-03-28_modified.jsonl"
#output_path = "data/dataset/train4000_2025-03-28_modified.jsonl"
#output_path = "data/dataset/val1000_2025-03-28_modified.jsonl"

# with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
#     for line in tqdm(infile):
#         if not line.strip():
#             continue
        
#         data = json.loads(line)

#         # Example: modify the target
#         try:
#             target = json.loads(data['messages'][2]['content'])
            
#             for table in tables:
#                 parameters = target[table]
#                 new_parameters = []
#                 for parameter in parameters:
#                     if len(parameter['values']) != 0:
#                         new_parameters.append(parameter)
#                     else:
#                         print(target['epd_id'])
                        
#                 target[table] = new_parameters
        
#             data['messages'][2]['content'] = json.dumps(target)

#         except (IndexError, KeyError, json.JSONDecodeError) as e:
#             print("Skipping malformed line:", e)
#             continue

#         # Write modified data back to the output file
#         outfile.write(json.dumps(data) + '\n')
        
        
for file_name in os.listdir("data/target"):
    file_path = os.path.join("data/target", file_name)
    
    with open(file_path, 'r') as file:
        target = json.load(file)
    
    #modify the target
    for table in tables:
        parameters = target[table]
        new_parameters = []
        for parameter in parameters:
            if 'Unit' in parameter.keys():
                del parameter['Unit']
                  
            new_parameters.append(parameter)
                
        target[table] = new_parameters
        
    json.dump(target, open(file_path, 'w'), indent=4)
