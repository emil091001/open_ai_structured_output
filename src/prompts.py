prompt_max = """ 
        ### Instruction: 
        You are a system that extracts data from PDF files into a structured JSON format. 
        You may only return raw JSON with no surrounding descriptory text. 
        Indivdual values should not be converted or changed from how they appear in the original text.
        if there are ambigious ones such as ADP-minerals&metals it must be mapped to the closest match i.e ADPM, ADPE is for ADP for non fossil and ADPF = ADP-fossil, WDP1 must be mapped to WDP, EP-FreshWater to EP-freshwater. GWP is just treated as GWP-total.
        There may be examples in any language, the shorthand versions may be written out explicitly.
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
        "ADPM",
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
    # STRUCTURE
    Module = Literal["A1-A3", "A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "C1", "C2", "C3", "C4", "D"]
    
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
    
    # Follow this structure:  
    class Value(BaseModel):
        value: str
        module: Module
    
    
    class Parameter[T](BaseModel):
        parameter: T
        unit: str
        values: List[Value]
    
    class Structure(BaseModel):
        product_name: str
        epd_id: str
        valid_to: str
        ref_year: str
        compliance: List[str]
        producer_name: str
        environmental_impact: List[Parameter[EnvironmentalImpactParameterName]]
        additional_environmental_impact: List[Parameter[AdditionalEnvironmentalImpactParameterName]]
        resource_use: List[Parameter[ResourceUseParameterName]]
        end_of_life_waste: List[Parameter[EndOfLifeWasteParameterName]]
        end_of_life_flow: List[Parameter[EndOfLifeFlowParameterName]]
    
    
    You may only return raw JSON with no surrounding descriptory text.
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
