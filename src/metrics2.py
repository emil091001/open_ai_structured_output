import json
import os
from typing import Any, List, Dict, Tuple, TypeVar
from config import PROMPT1
from pydantic import BaseModel
from structure import Parameter, Structure, Value
from tqdm import tqdm
from openai import AzureOpenAI
from dotenv import load_dotenv
from utils.float_conversion import convert_to_float
from utils.load_json import load_json


class Metrics:
    def compare_values(self, target_values: Value, output_values: Value):
        for target_value in target_values:
            for output_value in output_values:
                if not target_value.module == output_value.module:
                    continue

                target_value_float = convert_to_float(target_value.value)
                output_value_float = convert_to_float(output_value.value)

                if not target_value_float == output_value_float:
                    return False

        return True

    def compare_tables(
            self, target_params: List[Parameter], output_params: List[Parameter]) -> Tuple:
        true_positives = 0
        false_positives = 0
        false_negatives = 0

        output_dict = {param.parameter: param for param in output_params}
        target_dict = {param.parameter: param for param in target_params}

        false_positives_elements = []
        false_negatives_elements = []

        for target_param in target_params:
            output_param = output_dict.get(target_param.parameter)
            if output_param is None:
                false_negatives += 1
                false_negatives_elements.append(target_param.dict())
                continue

            if not self.compare_values(
                    target_param.values, output_param.values):
                false_negatives += 1
                false_negatives_elements.append(target_param.dict())
                continue

            true_positives += 1

        for output_param in output_params:
            target_param = target_dict.get(output_param.parameter)
            if target_param is None:
                false_positives += 1
                false_positives_elements.append(output_param.dict())
                continue

            if not self.compare_values(
                    target_param.values, output_param.values):
                false_positives += 1
                false_positives_elements.append(output_param.dict())
                continue

        return true_positives, false_positives, false_negatives, false_positives_elements, false_negatives_elements

    def calculate(
            self, target: Structure, output: Structure) -> Dict[str, Dict[str, float]]:
        results = {}
        tables = [
            'environmental_impact',
            'additional_environmental_impact',
            'resource_use',
            'end_of_life_waste',
            'end_of_life_flow']

        for table in tables:
            target_params = getattr(target, table)
            output_params = getattr(output, table)
            tp, fp, fn, false_positive_elements, false_negative_elements = self.compare_tables(
                target_params, output_params)

            precision = tp / (tp + fp) if tp + fp > 0 else 1.0
            recall = tp / (tp + fn) if tp + fn > 0 else 1.0

            results[table] = {
                'precision': precision,
                'recall': recall,
                'false_positives': false_positive_elements,
                'false_negatives': false_negative_elements
            }

        return results
    
    def calculate_average(self, target: Structure, output: Structure) -> Dict[str, Dict[str, float]]:
        metrics = self.calculate(target, output)
        avg_precision = sum([table['precision'] for table in metrics.values()]) / len(metrics)
        avg_recall = sum([table['recall'] for table in metrics.values()]) / len(metrics)
        
        return {
            'avg_precision': avg_precision,
            'avg_recall': avg_recall
        }


