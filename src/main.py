import os
from typing import List
from pydantic import BaseModel
from openai import AzureOpenAI
from dotenv import load_dotenv
from structure import Structure
import json
from config import *


load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY_BUILDTIVITY"),
    api_version="2024-08-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_BUILDTIVITY"),
)


with open("/Users/emilschneiderlorentzen/UNI/6sm/project/open_ai_structured_output/data/pdf/  Birsta S N2 W2 c_c 1 m.txt", "r") as file:
    testPdf = file.read()


def model(pdf: str) -> Structure:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{PROMPT1}"},
            {"role": "user", "content": f"{pdf}"},
        ],
        response_format=Structure,
        temperature=0.0,
    )

    return completion.choices[0].message.parsed


completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"{PROMPT1}"},
        {"role": "user", "content": f"{testPdf}"},
    ],
    response_format=Structure,
    temperature=0.0,
)


event = completion.choices[0].message.parsed.dict()

print(event)

with open("data/test_output.json", "w") as file:
    json.dump(event, file)
