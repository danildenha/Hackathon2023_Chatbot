import json


def save_language_choice(user_id, language):
    data = {}

    try:
        with open('answers/language_data.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    if str(user_id) in data:
        data[str(user_id)] = language
    else:
        data[str(user_id)] = language

    with open('answers/language_data.json', 'w') as file:
        json.dump(data, file)


def check_user_exists(user_id):
    try:
        with open('answers/language_data.json', 'r') as file:
            data = json.load(file)
            return str(user_id) in data
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def get_user_language(user_id):
    try:
        with open('answers/language_data.json', 'r') as file:
            data = json.load(file)
            return data.get(str(user_id))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_calls_choice(user_id, phone_call):
    data = {}

    try:
        with open('answers/howm_calls.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    if str(user_id) in data:
        data[str(user_id)] = phone_call
    else:
        data[str(user_id)] = phone_call

    with open('answers/howm_calls.json', 'w') as file:
        json.dump(data, file)


def get_user_calls(user_id):
    try:
        with open('answers/howm_calls.json', 'r') as file:
            data = json.load(file)
            return data.get(str(user_id))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_mobdata_choice(user_id, mob_data):
    data = {}

    try:
        with open('answers/howm_mobdata.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    if str(user_id) in data:
        data[str(user_id)] = mob_data
    else:
        data[str(user_id)] = mob_data

    with open('answers/howm_mobdata.json', 'w') as file:
        json.dump(data, file)


def get_user_mobdata(user_id):
    try:
        with open('answers/howm_mobdata.json', 'r') as file:
            data = json.load(file)
            return data.get(str(user_id))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_social_choice(user_id, social):
    data = {}

    try:
        with open('answers/social_member.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    if str(user_id) in data:
        data[str(user_id)] = social
    else:
        data[str(user_id)] = social

    with open('answers/social_member.json', 'w') as file:
        json.dump(data, file)


def get_user_social(user_id):
    try:
        with open('answers/social_member.json', 'r') as file:
            data = json.load(file)
            return data.get(str(user_id))
    except (FileNotFoundError, json.JSONDecodeError):
        return None




