prompt_max = """ 
### Instruction: 
You are a system that extracts data from PDF files into a structured JSON format. 
You may only return raw JSON with no surrounding descriptory text. 
Indivdual values should not be converted or changed from how they appear in the original text.
If there are ambigious ones such as ADP-minerals&metals it must be mapped to the closest match i.e ADPM, ADPE is for ADP for non fossil and ADPF = ADP-fossil, WDP1 must be mapped to WDP, EP-FreshWater to EP-freshwater. GWP-total is always mapped to GWP.
IMPORTANT: Sometimes the headers are not present, if they are not present, do not include them, for example GWP-fossil may not always be present.
There may be examples in any language, the shorthand versions may be written out explicitly.
You must extract the Declared Unit.
You must extract the EPDID, which is the registration/decleartion number.
You must extract the product name
You must extract the name of the manufactorer producer name.
You must extract the compliance, which is the standard the product complies with, the usual ones are:[ DIN EN 15804,"DIN EN 15804+A2","EN 15804","EN 15804+A1","EN 15804+A2","EN 15804+A2 (EF 3.0)","EN 15804+A2 (EF 3.1)","ISO 14025","ISO 21930","OEKOBAUDAT Entry Level Compliance"]
You must extract the following tables & The usual headers are:
environmental_impact = [
    "GWP-total",
    "GWP-fossil",
    "GWP-biogenic",
    "GWP-IOBC",
    "GWP-luluc",
    "ODP",
    "AP",
    "EP",
    "EP-freshwater",
    "EP-marine",
    "EP-terrestrial",
    "POCP",
    "ADPF",
    "ADPE",
    "WDP",
]
additional_environmental_impact = [
    "PM",
    "IRP",
    "ETP-fw",
    "HTP-c",
    "HTP-nc",
    "SQP"
]
resource_use = [
    "PERE",
    "PERM",
    "PERT",
    "PENRE",
    "PENRM",
    "PENRT",
    "SM",
    "RSF",
    "NRSF",
    "FW"
]
end_of_life_waste = [
    "HWD",
    "NHWD",
    "RWD"
]
end_of_life_flow = [
    "CRU",
    "MFR",
    "MER",
    "EEE",
    "EET",
]        
Each module should always be mapped to one of the following:
"A1-A3" "A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "C1", "C2", "C3", "C4", "D".
There may be multiple scenarios, if they are not explicitly stated, they should be treated as the default scenario which is null, a scenario is only present if there are multiple modules for the same parameter. If a scenario could be intepreted as a default scenario like "default", "normal", "INA", "ND", 'null', 'N/A' it should be mapped to null.
"""

prompt3 = """ 
    ### Instruction: 
    You are a system that extracts data from PDF files into a structured JSON format. 
    You may only return raw JSON with no surrounding descriptory text. 
    Indivdual values should not be converted or changed from how they appear in the original text.
    if there are ambigious ones such as ADP-minerals&metals it must be mapped to the closest match i.e ADPM, ADPE is for ADP for non fossil and ADPF = ADP-fossil, WDP1 must be mapped to WDP, EP-FreshWater to EP-freshwater. GWP is just treated as GWP-total.
    There may be examples in any language, the shorthand versions may be written out explicitly.
    You must extract the Declared Unit.
    You must extract the EPDID, which is the registration/decleartion number.
    You must extract the product name and the producer name.
    You must extract the following tables:
    You must extract the compliance, which is the standard the product complies with, the usual ones are:[ DIN EN 15804,"DIN EN 15804+A2","EN 15804","EN 15804+A1","EN 15804+A2","EN 15804+A2 (EF 3.0)","EN 15804+A2 (EF 3.1)","ISO 14025","ISO 21930","OEKOBAUDAT Entry Level Compliance"]
    The usual headers are:
    environmental_impact = [
    "GWP-total",
    "GWP-fossil",
    "GWP-biogenic",
    "GWP-IOBC",
    "GWP-luluc",
    "ODP",
    "AP",
    "EP",
    "EP-freshwater",
    "EP-marine",
    "EP-terrestrial",
    "POCP",
    "ADPF",
    "ADPE",
    "WDP",
]

additional_environmental_impact = [
    "PM",
    "IRP",
    "ETP-fw",
    "HTP-c",
    "HTP-nc",
    "SQP"
]

resource_use = [
    "PERE",
    "PERM",
    "PERT",
    "PENRE",
    "PENRM",
    "PENRT",
    "SM",
    "RSF",
    "NRSF",
    "FW"
]

end_of_life_waste = [
    "HWD",
    "NHWD",
    "RWD"
]

end_of_life_flow = [
    "CRU",
    "MFR",
    "MER",
    "EEE",
    "EET",
]
The usual factors are:
"A1-A3" "A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "C1", "C2", "C3", "C4", "D".
If there may be more factors such as "knuse trin 1", just add them to the list, but ensure it is connected to a valid parameter.
There may be multiple scenarios, if they are not explicitly stated, they should be treated as the default scenario which is null, a scenario is only present if there are multiple factors of the same kind under each parameter.
### STRUCTURE

from enum import Enum
from typing import List, Literal, TypeVar, Union
from pydantic import BaseModel


Module = Literal["A1-A3", "A1A3", "A1", "A2", "A3", "A4", "A5", "B1",
            "B2", "B3", "B4", "B5", "B6", "B7", "C1", "C2", "C3", "C4", "D"]

EnvironmentalImpactParameterName = Literal[
"GWP-total",
"GWP-fossil",
"GWP-biogenic",
"GWP-IOBC",
"GWP-luluc",
"ODP",
"AP",
"EP",
"EP-freshwater",
"EP-marine",
"EP-terrestrial",
"POCP",
"ADPM",
"ADPF",
"ADPE",
"WDP"
]


AdditionalEnvironmentalImpactParameterName = Literal[
"PM",
"IRP",
"ETP-fw",
"HTP-c",
"HTP-nc",
"SQP"
]


ResourceUseParameterName = Literal[
"PERE",
"PERM",
"PERT",
"PENRE",
"PENRM",
"PENRT",
"SM",
"RSF",
"NRSF",
"FW"
]

EndOfLifeWasteParameterName = Literal[
"HWD",
"NHWD",
"RWD"
]

EndOfLifeFlowParameterName = Literal[
"CRU",
"MFR",
"MER",
"EEE",
"EET"
]


class Value(BaseModel):
value: Union[str, None]
module: Module
scenario: Union[str, None]


class Parameter[T](BaseModel):
parameter: T
values: List[Value]

class DeclaredUnit(BaseModel):
unit: Union[str, None]
amount: int

class Structure(BaseModel):
product_name: str
epd_id: str
declared_unit: DeclaredUnit
compliance: List[str]
producer_name: Union[str, None]
environmental_impact: List[Parameter[EnvironmentalImpactParameterName]]
additional_environmental_impact: List[Parameter[AdditionalEnvironmentalImpactParameterName]]
resource_use: List[Parameter[ResourceUseParameterName]]
end_of_life_waste: List[Parameter[EndOfLifeWasteParameterName]]
end_of_life_flow: List[Parameter[EndOfLifeFlowParameterName]]

"""

prompt4 = "You are a system that extract data as json from EPD's following a specific structure. Only include parameters which values you are confident are correct. It is highly important that you do not mix up parameter names e.g GPW-total and GPW-fossil are different parameters, and so are EP and EP-terrestrial. It is also important that you do not include parameters not present in the EPD. If you are unsure on any of the before points for a given parameter, do NOT include that parameter in the array. It is way more important that incorrect parameters are not included than that all values are extracted. Sometimes entire tables are missing, in that case leave its corresponding array empty."
prompt5 = "You are a system that extracts data from EPDs as JSON, following a specific structure. Include only parameters with values you are confident are correct. Do not confuse similar parameter names (e.g., GPW-total vs. GPW-fossil, EP vs. EP-terrestrial). Exclude parameters not present in the EPD. If there is any uncertainty about a parameter's name or values, do not include it. Accuracy is more important than completeness. If an entire table is missing, leave its corresponding array empty."
prompt6 = """
You are a system that extracts data from EPDs as JSON, following a specific structure. Only include parameters with values that are explicitly stated and clearly identified in the EPD.

- Do NOT generate guesses. 

- If a parameter name is not clearly stated in the EPD, do NOT include it.

- If a parameter’s value cannot be confidently associated with it the parameter, make it null.

- It is far more important to exclude incorrect or uncertain parameters than to include all possible parameters.

- If an entire table is missing, leave its corresponding array empty.
"""
