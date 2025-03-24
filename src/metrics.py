import json
from typing import Dict, Any, List

from structure import Parameter


def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)


def convert_to_float(sci_str: str) -> float:
    formatted_str = sci_str.replace(',', '.')
    try:
        # Convert to float
        return float(formatted_str)
    except ValueError:
        raise ValueError(f"Invalid scientific notation string: {sci_str}")


def compare_values(target_values: List[Dict], output_values: List[Dict]):
    for target_value in target_values:
        for output_value in output_values:
            if not target_value['module'] == output_value['module']:
                continue

            target_value_float = convert_to_float(target_value['value'])
            output_value_float = convert_to_float(output_value['value'])

            if not target_value_float == output_value_float:
                return False

    return True


def compare_parameter_lists(
        target: List[Dict[str, Any]], output: List[Dict[str, Any]]):
    # Calculate precision
    if len(target) == 0 and len(output) == 0:
        return (1.0, [])

    elif len(target) == 0 and len(output) > 0:
        return (0.0, [])

    else:
        param_true_positives = 0
        param_false_positives = 0

        mis_matches = []
        for output_parameter in output:
            target_parameter = next(
                (p for p in target if p['parameter'] == output_parameter['parameter']), None)

            # If parameter is not found in target it is a false positives
            if target_parameter is None:
                param_false_positives += 1
                mis_matches.append(output_parameter)
                continue

            # If parameter is found in target but is not equal it is a false
            # positive
            if not compare_values(
                    target_parameter['values'],
                    output_parameter['values']):
                param_false_positives += 1
                mis_matches.append(output_parameter)
                continue
            # If parameter is found in target and is equal it is a true
            # positive
            param_true_positives += 1

        precision = param_true_positives / \
            (param_true_positives + param_false_positives) if param_true_positives + \
            param_false_positives != 0 else 1.0


def compare_dictionaries(
        target: Dict[str, Any], output: Dict[str, Any]) -> Dict[str, float]:
    metrics = {
        'table_precision': {},
        'table_recall': {},
    }

    for key in target.keys():
        # Skip if key is not a list
        if not isinstance(target[key], list):
            continue

        # Skip if list is not a parameter list
        for item in target[key]:
            try:
                Parameter.model_validate(item)
                break
            except Exception as e:
                continue

        # Calculate precision
        if len(target[key]) == 0 and len(output[key]) == 0:
            metrics['table_precision'] |= {key: {"precision": 1.0}}

        elif len(target[key]) == 0 and len(output[key]) > 0:
            metrics['table_precision'] |= {key: {"precision": 0.0}}

        else:
            param_true_positives = 0
            param_false_positives = 0
            precision_dict = {
                'precision': None,
                'false_positives': []
            }
            for output_parameter in output[key]:
                target_parameter = next(
                    (p for p in target[key] if p['parameter']
                     == output_parameter['parameter']),
                    None)

                # If parameter is not found in target it is a false positives
                if target_parameter is None:
                    param_false_positives += 1
                    precision_dict['false_positives'].append(output_parameter)
                    continue

                # If parameter is found in target but is not equal it is a
                # false positive
                if not compare_values(
                        target_parameter['values'],
                        output_parameter['values']):
                    param_false_positives += 1
                    precision_dict['false_positives'].append(output_parameter)
                    continue
                # If parameter is found in target and is equal it is a true
                # positive
                param_true_positives += 1

            precision = param_true_positives / \
                (param_true_positives + param_false_positives) if param_true_positives + \
                param_false_positives != 0 else 1.0
            precision_dict['precision'] = precision

            metrics['table_precision'] |= {key: precision_dict}

        # Calculate recall
        if len(target[key]) == 0 and len(output[key]) == 0:
            metrics['table_recall'] |= {key: {"recall": 1.0}}

        elif len(target[key]) > 0 and len(output[key]) == 0:
            metrics['table_recall'] |= {
                key: {
                    "recall": 0.0,
                    "false_negatives": target[key]}}

        else:
            param_true_positives = 0
            param_false_negatives = 0
            recall_dict = {
                'recall': None,
                'false_negatives': []
            }
            for target_parameter in target[key]:
                output_parameter = next(
                    (p for p in output[key] if p['parameter']
                     == target_parameter['parameter']),
                    None)

                # If parameter is not found in output it is a false negative
                if output_parameter is None:
                    param_false_negatives += 1
                    recall_dict['false_negatives'].append(target_parameter)
                    continue

                # If parameter is found in output but is not equal it is a
                # false negative
                if not compare_values(
                        target_parameter['values'],
                        output_parameter['values']):
                    param_false_negatives += 1
                    recall_dict['false_negatives'].append(target_parameter)
                    continue
                # If parameter is found in output and is equal it is a true
                # positive
                param_true_positives += 1

            recall = param_true_positives / \
                (param_true_positives + param_false_negatives) if param_true_positives + \
                param_false_negatives != 0 else 1.0
            recall_dict['recall'] = recall

            metrics['table_recall'] |= {key: recall_dict}

    return metrics


# Example usage
if __name__ == "__main__":
    ground_truth = load_json(
        '/Users/emilschneiderlorentzen/UNI/6sm/project/open_ai_structured_output/data/target/  Birsta S N2 W2 c_c 1 m.json')
    extracted = load_json(
        '/Users/emilschneiderlorentzen/UNI/6sm/project/open_ai_structured_output/data/test_output copy 2.json')
    metrics = compare_dictionaries(ground_truth, extracted)
    print(json.dumps(metrics, indent=4))
