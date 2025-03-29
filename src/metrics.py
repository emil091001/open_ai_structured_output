from typing import List, Dict, Tuple
from structure import Parameter, Structure, Value
from utils.float_conversion import convert_to_float


class Metrics:
    tables = [
        'environmental_impact',
        'additional_environmental_impact',
        'resource_use',
        'end_of_life_waste',
        'end_of_life_flow']

    primitive_properties = ['product_name', 'epd_id', 'producer_name']
    list_properties = ['compliance']
    dict_properties = ['declared_unit']

    def __init__(self, verbose=False):
        self.verbose = verbose
        
    def make_metric(self, precision, recall, false_positive_elements, false_negative_elements):
        
        if self.verbose:
            return {
                'precision': precision,
                'recall': recall,
                'false_positives': false_positive_elements,
                'false_negatives': false_negative_elements
            }
        else:
            return {
                'precision': precision,
                'recall': recall
            }
            
    def convert_scenario(self, value):
        none_types = ["INA", "ND", 'null', 'N/A']
        if value is None or value in none_types:
            return None
        
        return value

    def compare_values(self, target_values: List[Value], output_values: List[Value]):
        
        
        output_lookup = {hash((value.module, self.convert_scenario(value.scenario))): value for value in output_values}
        #output_lookup = {hash(value.module): value for value in output_values}

        tp = 0
        fn = 0

        for target_value in target_values:
            hash_value = hash((target_value.module, self.convert_scenario(target_value.scenario)))
            #hash_value = hash(target_value.module)
            output_value = output_lookup.get(hash_value)
            if output_value is None:
                fn += 1
                continue

            if convert_to_float(target_value.value) != convert_to_float(output_value.value):
                fn += 1
                continue
            
            tp += 1
            output_lookup.pop(hash_value)

        fp = len(output_lookup)
        
        precision = tp / (tp + fp) if tp + fp > 0 else 1.0
        recall = tp / (tp + fn) if tp + fn > 0 else 1.0

        

        return precision, recall

    def compare_tables(
            self, target_params: List[Parameter], output_params: List[Parameter]) -> Tuple:
  
        output_dict = {param.parameter: param for param in output_params}        
        false_negative_elements = []

        avg_precision = 0
        avg_recall = 0

        for target_param in target_params:
            output_param = output_dict.get(target_param.parameter)
            if output_param is None:
                false_negative_elements.append(target_param.model_dump())
                continue

            precision, recall = self.compare_values(target_param.values, output_param.values)
            avg_precision += precision
            avg_recall += recall

            output_dict.pop(target_param.parameter)

        avg_precision = avg_precision / len(output_params) if len(output_params) > 0 else 1.0
        avg_recall = avg_recall / len(target_params) if len(target_params) > 0 else 1.0
        
        false_positive_elements = list(param.model_dump() for param in output_dict.values())
        
            
        return self.make_metric(avg_precision, avg_recall, false_positive_elements, false_negative_elements)


    def compare_lists(self, target_list: List, output_list: List):
        false_negatives = []
        false_positives = output_list.copy()
        tp = 0
        fn = 0
        for target_item in target_list:
            if target_item not in output_list:
                fn += 1
                false_negatives.append(target_item)
            else:
                tp += 1
                false_positives.remove(target_item)

        fp = len(false_positives)

        precision = tp / (tp + fp) if tp + fp > 0 else 1.0
        recall = tp / (tp + fn) if tp + fn > 0 else 1.0

        return self.make_metric(precision, recall, false_positives, false_negatives)

    def calculate(self, target: Structure, output: Structure):
        metrics = {}
        
        for property in self.primitive_properties:
            if getattr(target, property) == getattr(output, property):
                metrics[property] = True
            else:
                metrics[property] = False

        for property in self.list_properties:
            target_list = getattr(target, property)
            output_list = getattr(output, property)
            metrics[property] = self.compare_lists(target_list, output_list)
            
        for property in self.dict_properties:
            target_dict = getattr(target, property).model_dump()
            output_dict = getattr(output, property).model_dump()
            metrics[property] = {}
            for key in target_dict:
                if target_dict[key] == output_dict[key]:
                    metrics[property][key] = True
                else:
                    metrics[property][key] = False

        for table in self.tables:
            target_table = getattr(target, table)
            output_table = getattr(output, table)
            metrics[table] = self.compare_tables(target_table, output_table)
        
        
        
        
        return metrics

    def calculate_table(
            self, target: Structure, output: Structure) -> Dict[str, Dict[str, float]]:

        results = {}

        for table in self.tables:
            target_params = getattr(target, table)
            output_params = getattr(output, table)
            tp, fp, fn, false_positive_elements, false_negative_elements = self.compare_tables(
                target_params, output_params)

            precision = tp / (tp + fp) if tp + fp > 0 else 1.0
            recall = tp / (tp + fn) if tp + fn > 0 else 1.0

            if self.verbose:
                results[table] = {
                    'precision': precision,
                    'recall': recall,
                    'false_positives': false_positive_elements,
                    'false_negatives': false_negative_elements
                }
            else:
                results[table] = {
                    'precision': precision,
                    'recall': recall
                }

        return results

    def average(self, metrics_list: List[Dict[str, any]]):
        averages = {}

        for metrics in metrics_list:
            for property in self.primitive_properties:
                averages[property] = averages.get(property, 0) + float(metrics[property])
            
            for property in self.list_properties:
                averages[property] = averages.get(property, {})
                averages[property]["precision"] = averages[property].get("precision", 0) + float(metrics[property]["precision"])
                averages[property]["recall"] = averages[property].get("recall", 0) + float(metrics[property]["recall"])
                
            for property in self.dict_properties:
                averages[property] = averages.get(property, {})
                for sub_property in metrics[property]:
                    averages[property][sub_property] = averages[property].get(sub_property, 0) + float(metrics[property][sub_property])
                
            for table in self.tables:
                table_metrics = metrics[table]
                averages[table] = averages.get(table, {})
                averages[table]["precision"] = averages[table].get("precision", 0) + float(table_metrics["precision"])
                averages[table]["recall"] = averages[table].get("recall", 0) + float(table_metrics["recall"])
            
        for property in self.primitive_properties:
            averages[property] = averages[property] / len(metrics_list)
        
        for property in self.list_properties:
            averages[property]["precision"] = averages[property]["precision"] / len(metrics_list)
            averages[property]["recall"] = averages[property]["recall"] / len(metrics_list)
            averages[property]["F1"] = 2 * (averages[property]["precision"] * averages[property]["recall"]) / (averages[property]["precision"] + averages[property]["recall"])
            
        for property in self.dict_properties:
            for sub_property in averages[property]:
                averages[property][sub_property] = averages[property][sub_property] / len(metrics_list)
            
        for table in self.tables:
            averages[table]["precision"] = averages[table]["precision"] / len(metrics_list)
            averages[table]["recall"] = averages[table]["recall"] / len(metrics_list)
            averages[table]["F1"] = 2 * (averages[table]["precision"] * averages[table]["recall"]) / (averages[table]["precision"] + averages[table]["recall"]) if averages[table]["precision"] + averages[table]["recall"] > 0 else 0
            
        return averages

