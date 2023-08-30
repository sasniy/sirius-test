import requests
import re

FIRST_TOKEN = "@@ПЕРВЫЙ@@"
SECOND_TOKEN = "@@ВТОРОЙ@@"


def query(input_text, API_URL, headers, db, user_id):
    parameters = get_parameters()
    options = get_options()
    full_text = get_full_text(input_text, db, user_id)
    payload = {"inputs": full_text, 'options': options, 'parameters': parameters}
    response = requests.post(API_URL, headers=headers, json=payload).json()[0]
    answer = response['generated_text']
    question, answer = preprocces_message(answer)
    answer = answer.replace(FIRST_TOKEN, '')
    answer = answer.replace(SECOND_TOKEN, '')
    return answer


def get_full_text(input_text, db, user_id):
    text = f'{FIRST_TOKEN} {input_text} {SECOND_TOKEN}'
    user_messages, bot_messages = db.get_context(user_id)
    user_messages = [f'{FIRST_TOKEN} {message}' for message in user_messages]
    bot_messages = [f'{SECOND_TOKEN} {message}' for message in bot_messages]
    context = list(zip(user_messages, bot_messages))[::-1]
    full_text = ''
    for first, second in context:
        full_text += first + second
    full_text += text
    return full_text


def preprocces_message(text):
    first_text = text.split(FIRST_TOKEN)[0]
    second_text = text.split(SECOND_TOKEN)[-1]
    return first_text, second_text


def get_options():
    use_cashe = False
    wait_for_model = True
    return {'use_cashe': use_cashe, 'wait_for_model': wait_for_model}


def get_parameters():
    return {
        'max_new_tokens': 40,
        'temperature': 1.2,
        'length_penalty': 1.0,
        'no_repeat_ngram_size': 2,
        'do_sample': True,
        'repetition_penalty': 1.2,
        'eos_token_id': 50257,
        'top_k': 50,
        'top_p': 0.95,
        'num_beams': 3,
        'num_return_sequences': 3
    }


def get_headers(HF_TOKEN):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    return headers
