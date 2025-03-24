import json
import os
from config import *
from tqdm import tqdm
import random


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


dataset = Preprocessor(PROMPT1, PDF_PATH, TARGET_PATH).process()
random.shuffle(dataset)
train_set = dataset[:TRAIN_SIZE]
val_set = dataset[TRAIN_SIZE:TRAIN_SIZE + VAL_SIZE]
test_set = dataset[TRAIN_SIZE + VAL_SIZE:]


# Save train set to train.jsonl
with open("data/dataset/train1000.jsonl", "w") as train_file:
    for entry in train_set:
        train_file.write(json.dumps(entry) + "\n")

# Save validation set to val.jsonl
with open("data/dataset/val200.jsonl", "w") as val_file:
    for entry in val_set:
        val_file.write(json.dumps(entry) + "\n")


# Save test set to test.jsonl
with open("data/dataset/test.jsonl", "w") as test_file:
    for entry in test_set:
        test_file.write(json.dumps(entry) + "\n")

print("Preprocessing done!")
