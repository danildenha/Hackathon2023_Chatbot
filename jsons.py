import json

def save_language_choice(user_id, language):
    data = {}
    
    try:
        with open('user_answers.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    data[str(user_id)] = {"language": language}
    
    with open('user_answers.json', 'w') as file:
        json.dump(data, file)


def get_user_language(user_id):
    try:
        with open('user_answers.json', 'r') as file:
            data = json.load(file)
            user_data = data.get(str(user_id))
            if user_data:
                return user_data.get("language")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_calls_choice(user_id, phone_call):
    data = {}
    
    try:
        with open('user_answers.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    user_data = data.get(str(user_id), {})
    user_data["phone_call"] = phone_call
    data[str(user_id)] = user_data
    
    with open('user_answers.json', 'w') as file:
        json.dump(data, file)


def get_user_calls(user_id):
    try:
        with open('user_answers.json', 'r') as file:
            data = json.load(file)
            user_data = data.get(str(user_id))
            if user_data:
                return user_data.get("phone_call")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_mobdata_choice(user_id, mob_data):
    data = {}
    
    try:
        with open('user_answers.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    user_data = data.get(str(user_id), {})
    user_data["mob_data"] = mob_data
    data[str(user_id)] = user_data
    
    with open('user_answers.json', 'w') as file:
        json.dump(data, file)


def get_user_mobdata(user_id):
    try:
        with open('user_answers.json', 'r') as file:
            data = json.load(file)
            user_data = data.get(str(user_id))
            if user_data:
                return user_data.get("mob_data")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_social_choice(user_id, social):
    data = {}
    
    try:
        with open('user_answers.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    user_data = data.get(str(user_id), {})
    user_data["social"] = social
    data[str(user_id)] = user_data
    
    with open('user_answers.json', 'w') as file:
        json.dump(data, file)


def get_user_social(user_id):
    try:
        with open('user_answers.json', 'r') as file:
            data = json.load(file)
            user_data = data.get(str(user_id))
            if user_data:
                return user_data.get("social")
    except (FileNotFoundError, json.JSONDecodeError):
        return None
