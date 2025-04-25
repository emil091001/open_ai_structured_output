
import asyncio
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from structure import Structure
import json
from config import *
from tqdm import tqdm
from prompts import *

load_dotenv()


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-10-21",
)


async def generate(pdf: str):
    """Runs the synchronous API call asynchronously using asyncio.to_thread."""
    return await asyncio.to_thread(_sync_generate, pdf)


def _sync_generate(pdf: str):
    """Synchronous function that calls the OpenAI API."""
    completion = client.beta.chat.completions.parse(
        model=os.getenv("AZURE_OPENAI_MODEL_NAME"),
        messages=[
            {"role": "system", "content": prompt_max},
            {"role": "user", "content": pdf}
        ],
        response_format=Structure,
        temperature=0.0,
        logprobs=True
    )
    return completion.choices[0].logprobs.to_dict()


async def process_example(line, example_number):
    """Processes a single example asynchronously and prints progress."""
    if line.strip():
        test_example = json.loads(line)
        file_name = json.loads(test_example['messages'][2]['content'])[
            'epd_id'] + ".json"

        print(f"⏳ Processing example {example_number}...")

        output = await generate(test_example['messages'][1]['content'])

        file_path = os.path.join(OUTPUT_PATH, file_name)
        os.makedirs(OUTPUT_PATH, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as output_file:
            json.dump(output, output_file)

        return file_name, example_number



async def process_pdf(pdf, file_name, i):
    """Processes a single example asynchronously and prints progress."""
    print(f"⏳ Processing example {i}: {file_name}...")
    
    output = await generate(pdf)

    file_path = os.path.join(OUTPUT_PATH, file_name)
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as output_file:
        json.dump(output, output_file)

    return file_name, i

async def main():
    print("🚀 Generating structured outputs...")

    # # Read and filter non-empty lines
    # with open(TEST_PATH, "r", encoding='utf-8') as file:
    #     lines = [line.strip() for line in file if line.strip()][:100]
    
    pdfs = [(open(os.path.join('data/pdf', file_name.replace('.json', '.txt')), 'r').read(), file_name) for file_name in os.listdir('data/nice_epds') if file_name.endswith('.json')]

    tasks = [asyncio.create_task(process_pdf(pdf, file_name, i))
             for i, (pdf, file_name) in enumerate(pdfs, 1)]

    # Process results as they complete
    for task in asyncio.as_completed(tasks):
        try:
            file_name, example_number = await task  # Wait for the task to finish
            print(f"✅ Completed example {example_number}: {file_name}")
        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"✅ All examples processed!")

if __name__ == "__main__":
    asyncio.run(main())
