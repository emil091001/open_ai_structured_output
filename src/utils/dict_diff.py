
from typing import Union


def calc_diff(a: Union[dict, int, float], b: Union[dict, int, float]) -> dict:
    diff = {}
    
    if isinstance(a, (int, float)):
        if isinstance(b, (int, float)):
            return a - b
        else:
            raise ValueError(f"Type mismatch: {type(a)} and {type(b)}")
    
    
    for key in a:
        b_val = b.get(key)
        if b_val is None:
            raise ValueError(f"Key {key} not found in b")
        a_val = a[key]
        b_val = b[key]
        
        
        diff[key] = calc_diff(a_val, b_val)    
    
    return diff