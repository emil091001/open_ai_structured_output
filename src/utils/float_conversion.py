from typing import Union


def convert_to_float(sci_str: Union[str, None]) -> Union[float, None]:
    none_types = ["INA", "ND", 'null', 'N/A']

    if sci_str is None or sci_str in none_types:
        return None

    formatted_str = sci_str.replace(',', '.')
    try:
        # Convert to float
        return float(formatted_str)
    except ValueError:
        #raise ValueError(f"Invalid scientific notation string: {sci_str}")
        return None
