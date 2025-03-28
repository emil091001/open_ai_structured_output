
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

# client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY_FINE_TUNED"),
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_FINE_TUNED"),
#     api_version="2024-10-21",
# )


# def generate(pdf: str) -> Structure:
#     completion = client.beta.chat.completions.parse(
#         model=os.getenv("AZURE_OPENAI_MODEL_NAME_FINE_TUNED"),
#         messages=[
#             {"role": "system", "content": prompt4},
#             {"role": "user", "content": pdf}
#         ],
#         response_format=Structure,
#         temperature=0.0,
#     )

#     return completion.choices[0].message.parsed.model_dump()


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY_FINE_TUNED"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_FINE_TUNED"),
    api_version="2024-10-21",
)


# def generate(pdf: str) -> Structure:
#     completion = client.beta.chat.completions.parse(
#         model='gpt-4o-mini',
#         messages=[
#             {"role": "system", "content": prompt4},
#             {"role": "user", "content": pdf}
#         ],
#         response_format=Structure,
#         temperature=0.0,
#     )

#     return completion.choices[0].message.parsed.model_dump()

# if __name__ == "__main__":
#     print("Generating structured outputs...")

#     with open(TEST_PATH, "r", encoding='utf-8') as file:
#         count = 0
#         for line in file:
#             if line.strip():
#                 count += 1
#                 print(f"Generating structured output for example {count}...")
#                 test_example = json.loads(line)
#                 file_name = json.loads(test_example['messages'][2]['content'])[
#                     'epd_id'] + ".json"

#                 output = generate(test_example['messages'][1]['content'])

#                 file_path = os.path.join(OUTPUT_PATH, file_name)
#                 os.makedirs(OUTPUT_PATH, exist_ok=True)

#                 with open(file_path, "w", encoding="utf-8") as output_file:
#                     json.dump(output, output_file)

#                 break


async def generate(pdf: str):
    """Runs the synchronous API call asynchronously using asyncio.to_thread."""
    return await asyncio.to_thread(_sync_generate, pdf)


def _sync_generate(pdf: str):
    """Synchronous function that calls the OpenAI API."""
    completion = client.beta.chat.completions.parse(
        model=os.getenv("AZURE_OPENAI_MODEL_NAME_FINE_TUNED"),
        messages=[
            {"role": "system", "content": prompt4},
            {"role": "user", "content": pdf}
        ],
        response_format=Structure,
        temperature=0.0,
    )
    return completion.choices[0].message.parsed.model_dump()


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


async def main():
    print("🚀 Generating structured outputs...")

    # Read and filter non-empty lines
    with open(TEST_PATH, "r", encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()][:100]

    tasks = [asyncio.create_task(process_example(line, i))
             for i, line in enumerate(lines, 1)]

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
