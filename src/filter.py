
import json
import os
from config import *
from metrics import Metrics
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
        value_hashes = set()
        parameter_names = set()
        initial_modules = None
        n_removed_params = 0
        n_values = None
        for table in self.tables:
            parameters = getattr(filtered_output, table)
            filtered_parameters = {self.hash_param(parameter): parameter.copy() for parameter in parameters}
            all_zero_count = 0
            for parameter in parameters:
                value_hash = hash(str(parameter.values))
                parameter_hash = self.hash_param(parameter)

                if self.all_values_zero(parameter.values):
                    all_zero_count += 1

                # Do not include parameters with the same values as preveously included parameters
                # if value_hash in value_hashes and not self.all_values_zero(parameter.values):
                #     continue

                if parameter.parameter in parameter_names:
                    filtered_parameters.pop(parameter_hash)
                    continue

                current_n_values = len(
                    [value.module for value in parameter.values])

                if n_values is None:
                    n_values = current_n_values
                    
                if initial_modules is None:
                    initial_modules = {value.module for value in parameter.values}
                    
                for value in parameter.values:
                    if value.module not in initial_modules:
                        filtered_parameters[parameter_hash].values.remove(value)

                # if n_values != current_n_values:
                #     continue

                parameter_names.add(parameter.parameter)
                value_hashes.add(value_hash)

            # print(table, len(filtered_parameters), all_zero_count)
            if len(filtered_parameters) >= self.min_param_count and all_zero_count != len(parameters):
                n_removed_params += len(parameters) - len(filtered_parameters)
                setattr(filtered_output, table, filtered_parameters.values())
            else:
                n_removed_params += len(parameters)
                setattr(filtered_output, table, [])

        return n_removed_params, filtered_output
    def hash_param(self, param):
        return hash(str(param.model_dump()))

    def all_values_zero(self, values):
        for value in values:
            float_value = convert_to_float(value.value)
            if float_value != 0:
                return False
        return True


# output = Structure.parse_file('data/test_output copy.json')
# target = Structure.parse_file('data/test_target.json')
# output = Structure.parse_file('data/output/EPD-ALW-201900185-IBC1-DE.json')
# target = Structure.parse_file('data/target/EPD-ALW-201900185-IBC1-DE.json')

# metrics = Metrics()
# metrics_traw = metrics.calculate(target, output)
# #metrics_raw = metrics.calculate_average(target, output)

# filter = Filter()
# _, filtered_output = filter(output)
# metrics_filtered = metrics.calculate(target, filtered_output)
# #metrics_filtered = metrics.calculate_average(target, filtered_output)


# #print(json.dumps(filtered_output.model_dump(), indent=4))
# #print(json.dumps(metrics_raw, indent=4))
# #print(filtered_averages)
# print(json.dumps(metrics_raw, indent=4))
# print(json.dumps(metrics_filtered, indent=4))

# with open('data/filtered_output/Schiebeläden aus Holz.json', 'w') as f:
#     json.dump(filtered_output.model_dump(), f, indent=4)


filter = Filter(min_param_count=0)
metrics = Metrics(verbose=True)

metric_list = []

for file_name in tqdm(os.listdir("data/output")[:1000]):
    target_path = os.path.join(TARGET_PATH, file_name)
    output_path = os.path.join("data/output", file_name)
    target = Structure.parse_file(target_path)
    output = Structure.parse_file(output_path)

    n_removed_params, filtered_output = filter(output)


    metric = metrics.calculate(target, filtered_output)
    
    # if metric['additional_environmental_impact']['recall'] != 1:
    #     with open(f'data/metrics/{file_name}', 'w') as f:
    #         json.dump(metric, f, indent=4)
            
    #     break
    
    metric_list.append(metric)


average_metrics = metrics.average(metric_list)

print(json.dumps(average_metrics, indent=4))