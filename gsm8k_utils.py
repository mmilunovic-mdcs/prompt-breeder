import re
import json

def read_jsonl(path: str):
    with open(path) as fh:
        return [json.loads(line) for line in fh.readlines() if line]

# def gsm_extract_answer(completion):
#     match = re.search(r"#### (\-?[0-9\.\,]+)", completion)
#     return match.group(1).strip() if match else "[invalid]"

def gsm_extract_answer(answer):
    """Extract the answer from the GSM8k dataset format."""
    match = re.search(r"#### (\-?[0-9\.\,]+)", answer)
    return match.group(1).strip() if match else None

def check_answer_in_response(model_answer, expected_answer):
    """Check if the expected answer is present in the model's response."""
    return bool(re.search(re.escape(expected_answer), model_answer))