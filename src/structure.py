from enum import Enum
from typing import List, Literal, TypeVar, Union
from pydantic import BaseModel


Module = Literal["A1-A3", "A1", "A2", "A3", "A4", "A5", "B1",
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
    "IR",
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
    epd_id: Union[str, None]
    declared_unit: DeclaredUnit
    compliance: List[str]
    producer_name: Union[str, None]
    environmental_impact: List[Parameter[EnvironmentalImpactParameterName]]
    additional_environmental_impact: List[Parameter[AdditionalEnvironmentalImpactParameterName]]
    resource_use: List[Parameter[ResourceUseParameterName]]
    end_of_life_waste: List[Parameter[EndOfLifeWasteParameterName]]
    end_of_life_flow: List[Parameter[EndOfLifeFlowParameterName]]
