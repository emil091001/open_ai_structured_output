import json
import os
from config import *
from tqdm import tqdm
import random
from datetime import datetime
from prompts import *



class Preprocessor():
    def __init__(self, system_prompt, pdf_path, target_path):
        self.system_prompt = system_prompt
        self.pdf_path = pdf_path
        self.target_path = target_path

    def process(self):
        dataset = []
        for file_name in tqdm(os.listdir(self.target_path)):
            with open(os.path.join(self.target_path, file_name), "r", encoding="utf-8") as file:
                target = json.dumps(json.load(file))

            with open(os.path.join(self.pdf_path, file_name.replace(".json", ".txt")), "r", encoding="utf-8") as file:
                pdf = file.read()

            dataset.append(
                {
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": pdf},
                        {"role": "assistant", "content": target}]
                }
            )
        return dataset


dataset = Preprocessor(prompt_max, PDF_PATH, TARGET_PATH).process()


test_ids = [name.replace('.json', '') for name in os.listdir("data/nice_epds")]
train_ids = [json.loads(json.loads(line)["messages"][2]["content"])['epd_id'] for line in open('data/dataset/train_real_0.jsonl', 'r', encoding='utf-8')]
val_ids = [json.loads(json.loads(line)["messages"][2]["content"])['epd_id'] for line in open('data/dataset/val_real_0.jsonl', 'r', encoding='utf-8')]

test_subset = [d for d in dataset if json.loads(d["messages"][2]["content"])['epd_id'] in test_ids]
train_subset = [d for d in dataset if json.loads(d["messages"][2]["content"])['epd_id'] in train_ids]
val_subset = [d for d in dataset if json.loads(d["messages"][2]["content"])['epd_id'] in val_ids]
dataset = [d for d in dataset if json.loads(d["messages"][2]["content"])['epd_id'] not in test_ids + train_ids + val_ids]




random.shuffle(dataset)
train_set = dataset[:TRAIN_SIZE - len(train_subset)] + train_subset
val_set = dataset[TRAIN_SIZE:TRAIN_SIZE + VAL_SIZE - len(val_subset)] + val_subset
test_set = dataset[TRAIN_SIZE + VAL_SIZE:] + test_subset

random.shuffle(train_set)
random.shuffle(val_set)
random.shuffle(test_set)


time_stamp = datetime.today().strftime('%Y-%m-%d')

# Save train set to train.jsonl
with open(f"data/dataset/train{TRAIN_SIZE}_{time_stamp}.jsonl", "w") as train_file:
    for entry in train_set:
        train_file.write(json.dumps(entry) + "\n")

# Save validation set to val.jsonl
with open(f"data/dataset/val{VAL_SIZE}_{time_stamp}.jsonl", "w") as val_file:
    for entry in val_set:
        val_file.write(json.dumps(entry) + "\n")


# Save test set to test.jsonl
with open(f"data/dataset/test{time_stamp}.jsonl", "w") as test_file:
    for entry in test_set:
        test_file.write(json.dumps(entry) + "\n")

print("Preprocessing done!")
