import requests
import re


def query(input_text, API_URL, headers, db, user_id):
    text = input_text
    parameters = get_parameters()
    options = get_options()
    user_messages, bot_messages = db.get_context(user_id)

    payload = {"inputs": {
        "past_user_inputs": user_messages,
        "generated_responses": bot_messages,
        "text": f'{text}'}, 'options': options, 'parameters': parameters}
    # payload = {"inputs": f'@@ПЕРВЫЙ@@ Привет @@ВТОРОЙ@@ привет @@ПЕРВЫЙ@@ {text} @@ВТОРОЙ@@','options':options,'parameters':parameters}
    response = requests.post(API_URL, headers=headers, json=payload).json()
    print(response)
    answer = response['generated_text']
    answer = answer.replace('@@ПЕРВЫЙ@@', '')
    answer = answer.replace('@@ВТОРОЙ@@', '')
    return answer


def get_options():
    use_cashe = False
    wait_for_model = True
    return {'use_cashe': use_cashe, 'wait_for_model': wait_for_model}


def get_parameters():
    return {
        'temperature': 1.0,
        'length_penalty': 1.0,
        'no_repeat_ngram_size': 2,
        'eos_token_id':50257,
        'do_sample':True,
        'max_new_tokens':40
    }


def get_headers(HF_TOKEN):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    return headers
