# post processing functions
import re
import json


    
def tokenize_text(text):
    """Tokenize the input text into a list of tokens."""
    return re.findall(r'\w+(?:[-_]\w+)*|\S', text)


def extract_entities(data):
    """Extracts entity spans from an entry."""

    all_examples = []

    for dt in data:
        # Tokenize the input text
        try:
            tokens = tokenize_text(dt['text'])  # Tokenized text
            ents = [
                (entity, entity_type)  # Flatten dictionary to list of tuples
                for entity_type, entity_list in dt['label'].items()
                for entity in entity_list
            ]
        except Exception as e:
            print(f"Error processing record: {e}")
            continue

        spans = []
        for entity, entity_type in ents:
            entity_tokens = tokenize_text(entity)

            # Find the start and end indices of each entity in the tokenized text
            for i in range(len(tokens) - len(entity_tokens) + 1):
                if " ".join(tokens[i:i + len(entity_tokens)]).lower() == " ".join(entity_tokens).lower():
                    spans.append((i, i + len(entity_tokens) - 1, entity_type.lower()))
        print(spans)
        # Append the tokenized text and its corresponding named entity recognition data
        all_examples.append({"tokenized_text": tokens, "ner": spans})

    return all_examples

def save_data_to_file(data, filepath):
    """Saves the processed data to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    # 从 JSON 文件加载
    with open("/Users/yunyunzhao/Desktop/01/Agri_NER/data/test.json", "r", encoding="utf-8") as f:
        data = json.load(f)  # `data` 是一个 Python 列表或字典
        
    processed_data = extract_entities(data)

    save_data_to_file(processed_data, "gliner_test.json")
    print("dataset size:", len(processed_data))

