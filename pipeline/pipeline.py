from inspect import getsource, getmembers, isfunction
import json
import random
from pathlib import Path

# Parameters

# replace f_file with the name of .py file containing functions
import f_file as functions

DATASET_NAME = "list_20"
DATA_SIZE = 20
EXAMPLES_PER_TASK = 30
SEED = 1984
MIN_LIST_LENGTH = 2
MAX_LIST_LENGTH = 5
LIST_DEFINITION_SPACE = range(100)

# Initialization

function_list = getmembers(functions, isfunction)

train_data_path = "data/tasks/" + DATASET_NAME + "/train"
train_language_data_path = "data/language/" + DATASET_NAME + "/train"
test_data_path = "data/tasks/" + DATASET_NAME + "/test"
test_language_data_path = "data/language/" + DATASET_NAME + "/test"
for path in [
    train_data_path,
    train_language_data_path,
    test_data_path,
    test_language_data_path,
]:
    Path(path).mkdir(parents=True, exist_ok=True)

random.seed(SEED)
task_names_iterators = {}


def generate_data():
    examples_data = []
    language_data = {}
    vocab_data = set()

    for _ in range(DATA_SIZE):
        (function_name, function) = random.choice(function_list)
        if function_name not in task_names_iterators.keys():
            task_names_iterators[function_name] = 0
        task_name = function_name + str(task_names_iterators[function_name])
        task_names_iterators[function_name] += 1
        examples = []
        for _ in range(EXAMPLES_PER_TASK):
            list_len = random.randint(MIN_LIST_LENGTH, MAX_LIST_LENGTH)
            input = random.sample(LIST_DEFINITION_SPACE, list_len)
            output = function(input)
            examples.append({"i": input, "o": output})
        examples_data.append(
            {
                "type": {"input": "list-of-int", "output": "list-of-int"},
                "name": task_name,
                "examples": examples,
            }
        )
        language_data[task_name] = getsource(function)

    for source_code in language_data.values():
        source_code = source_code.split(" ")
        for word in source_code:
            vocab_data.add(word)
    if "" in vocab_data:
        vocab_data.remove("")
    vocab_data = list(vocab_data)

    return examples_data, language_data, vocab_data


train_data, train_language, train_vocab = generate_data()
with open(train_data_path + "/tasks.json", "w") as outfile:
    json.dump(train_data, outfile)
with open(train_language_data_path + "/language.json", "w") as outfile:
    json.dump(train_language, outfile)
with open(train_language_data_path + "/vocab.json", "w") as outfile:
    json.dump(train_vocab, outfile)

test_data, test_language, test_vocab = generate_data()
with open(test_data_path + "/tasks.json", "w") as outfile:
    json.dump(test_data, outfile)
with open(test_language_data_path + "/language.json", "w") as outfile:
    json.dump(test_language, outfile)
with open(test_language_data_path + "/vocab.json", "w") as outfile:
    json.dump(test_vocab, outfile)