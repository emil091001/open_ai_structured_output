from typing import Union


def convert_to_float(sci_str: Union[str, None]) -> Union[float, None]:
    if sci_str is None:
        return None
    
    formatted_str = sci_str.replace(',', '.')
    try:
        # Convert to float
        return float(formatted_str)
    except ValueError:
        raise ValueError(f"Invalid scientific notation string: {sci_str}")