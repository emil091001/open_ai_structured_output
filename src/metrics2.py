from collections import defaultdict
from structure import Structure
from utils.float_conversion import convert_to_float


class Metric:
    parameters = ['GWP-total', 'GWP-fossil', 'GWP-biogenic', 'GWP-luluc', 'ODP', 'AP',
       'POCP', 'ADPE', 'ADPF', 'WDP', 'EP-freshwater', 'EP-marine',
       'EP-terrestrial', 'PM', 'ETP-fw', 'HTP-c', 'HTP-nc', 'SQP', 'IRP',
       'PERE', 'PERM', 'PERT', 'PENRE', 'PENRM', 'PENRT', 'SM', 'RSF', 'NRSF',
       'HWD', 'NHWD', 'RWD', 'CRU', 'MFR', 'MER', 'EEE', 'EET', 'FW', 'EP',
       'GWP-IOBC']

    modules = ["A1",	"A2",	"A3",	"A1-A3", "A4",	"A5",	"B1",	"B2",	"B3",	"B4",	"B5",	"B6",	"B7",	"C1",	"C2",	"C3",	"C4",	"D"]
    
    tables = [
        'environmental_impact',
        'additional_environmental_impact',
        'resource_use',
        'end_of_life_waste',
        'end_of_life_flow']
    
    def __init__(self):
        self.tp = defaultdict(lambda: defaultdict(int))
        self.fp = defaultdict(lambda: defaultdict(int))
        self.fn = defaultdict(lambda: defaultdict(int))
    
    def format(self, s: Structure):
        values = dict()
        
        for table in self.tables:
            target_table = getattr(s, table)
            
            for parameter in target_table:
                for value in parameter.values:
                    name = parameter.parameter
                    module = value.module
                    value = value.value
                    
                    values[name] = values.get(name, {})
                    values[name][module] = value
                    
        return values
        
    def add(self, target: Structure, output: Structure):
        target = self.format(target)
        output = self.format(output)
        
        for parameter in self.parameters:
            for module in self.modules:
                target_value = target.get(parameter, {}).get(module, None)
                output_value = output.get(parameter, {}).get(module, None)
                
                if convert_to_float(target_value) == convert_to_float(output_value) and target_value is not None:
                    self.tp[parameter][module] += 1
                
                if convert_to_float(target_value) != convert_to_float(output_value) and output_value is not None:
                    self.fp[parameter][module] = self.fp.get(parameter, {}).get(module, 0) + 1
                
                if convert_to_float(target_value) != convert_to_float(output_value) and target_value is not None:
                    self.fn[parameter][module] = self.fn.get(parameter, {}).get(module, 0) + 1
    
    def calculate(self):
        precision = defaultdict(lambda: defaultdict(float))
        recall = defaultdict(lambda: defaultdict(float))
        f1 = defaultdict(lambda: defaultdict(float))
        
        for parameter in self.parameters:
            for module in self.modules:
                tp = self.tp[parameter][module]
                fp = self.fp[parameter][module]
                fn = self.fn[parameter][module]
                
                if tp + fp == 0:
                    precision[parameter][module] = 1
                else:
                    precision[parameter][module] = tp / (tp + fp)
                
                if tp + fn == 0:
                    recall[parameter][module] = 1
                else:
                    recall[parameter][module] = tp / (tp + fn)
                    
                if precision[parameter][module] + recall[parameter][module] == 0:
                    f1[parameter][module] = 1
                else:
                    f1[parameter][module] = (2 * precision[parameter][module] * recall[parameter][module]) / (precision[parameter][module] + recall[parameter][module])
        
        return precision, recall, f1