import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json


bot = Bot(token="6141417763:AAE8EH-x1TLaGh_MCrK4aIXzrvvSV3PQFGc")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def save_language_choice(user_id, language):
    data = {}

    try:
        with open('language_data.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    if str(user_id) in data:
        data[str(user_id)] = language
    else:
        data[str(user_id)] = language

    with open('language_data.json', 'w') as file:
        json.dump(data, file)


def check_user_exists(user_id):
    try:
        with open('language_data.json', 'r') as file:
            data = json.load(file)
            return str(user_id) in data
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def get_user_language(user_id):
    try:
        with open('language_data.json', 'r') as file:
            data = json.load(file)
            return data.get(str(user_id))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    name = message.from_user.full_name
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, 'typing')
    await asyncio.sleep(0.5)

    lang_keyboard = types.InlineKeyboardMarkup()
    lang_keyboard.add(types.InlineKeyboardButton(text="Українська🇺🇦", callback_data="lang_ua"),
                      types.InlineKeyboardButton(text="English🇬🇧", callback_data="lang_en"))

    if check_user_exists(user_id):
        await start_taryf(message)
    else:
        await message.reply(f"""Привіт *{name}*, будьласка обери мову!  
Hi *{name}*, please choose your language!""",
                            reply_markup=lang_keyboard, parse_mode="Markdown")


@dp.message_handler(commands=['language'])
async def change_lang(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, 'typing')
    await asyncio.sleep(0.5)
    lang_keyboard = types.InlineKeyboardMarkup()
    lang_keyboard.add(types.InlineKeyboardButton(text="Українська🇺🇦", callback_data="lang_ua"),
                      types.InlineKeyboardButton(text="English🇬🇧", callback_data="lang_en"))

    await message.reply(f"""Будь ласка обери мову!  
Please choose your language!""",
                        reply_markup=lang_keyboard, parse_mode="Markdown")


async def start_taryf(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.full_name
    user_language = get_user_language(user_id)

    if user_language == "ua":
        start_keyboard_ua = types.InlineKeyboardMarkup()
        start_keyboard_ua.add(types.InlineKeyboardButton(text="🔎Підібрати тариф", callback_data="age_survey"),
                              types.InlineKeyboardButton(text="🌐Всі тарифи",
                                                         url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/"))
        await bot.send_message(user_id, f"Привіт *{name}*! Я допоможу тобі знайти найкращий для тебе тариф Lifecell!",
                               reply_markup=start_keyboard_ua, parse_mode="Markdown")

    elif user_language == "en":
        start_keyboard_en = types.InlineKeyboardMarkup()
        start_keyboard_en.add(types.InlineKeyboardButton(text="🔎Start selection", callback_data="age_survey"),
                              types.InlineKeyboardButton(text="🌐All tariffs",
                                                         url="https://www.lifecell.ua/en/mobile/tariffs/"))
        await bot.send_message(user_id, f"Hello *{name}*! I will help you to find the best Lifecell tariff!",
                               reply_markup=start_keyboard_en, parse_mode="Markdown")


@dp.callback_query_handler(lambda call: call.data == 'age_survey')
async def age_select(call: types.CallbackQuery):
    name = call.from_user.full_name
    user_id = call.from_user.id
    user_language = get_user_language(user_id)

    if user_language == "ua":
        understood_keyboard_ua = types.InlineKeyboardMarkup()
        understood_keyboard_ua.add(types.InlineKeyboardButton(text="✅Зрозуміло", callback_data="understood"))

        await call.message.edit_text(
            text=f"*{name}*, щоб підібрати найкращий тариф вам потрібно відповісти на декілька запитань.",
            reply_markup=understood_keyboard_ua, parse_mode="Markdown")

    elif user_language == "en":
        understood_keyboard_en = types.InlineKeyboardMarkup()
        understood_keyboard_en.add(types.InlineKeyboardButton(text="✅Understood", callback_data="understood"))

        await call.message.edit_text(
            text=f"*{name}*, to choose the best tariff, you need to answer a few simple questions.",
            reply_markup=understood_keyboard_en, parse_mode="Markdown")




@dp.callback_query_handler(lambda call: call.data == 'understood')
async def undersood_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_language = get_user_language(user_id)

    if user_language == "ua":
        less_than_eighteen = types.InlineKeyboardButton(text="Менше 18", callback_data="less_than_eighteen")
        more_than_eighteen = types.InlineKeyboardButton(text="Більше 18", callback_data="more_than_eighteen")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="back")

        age_keyboard = types.InlineKeyboardMarkup()
        age_keyboard.row(less_than_eighteen, more_than_eighteen)
        age_keyboard.row(back_button)

        await call.message.edit_text(text="""*Перше запитання*:
Будьласка оберіть ваш вік.""", reply_markup=age_keyboard, parse_mode="Markdown")
    elif user_language == "en":
        less_than_eighteen = types.InlineKeyboardButton(text="Less than 18", callback_data="less_than_eighteen")
        more_than_eighteen = types.InlineKeyboardButton(text="More than 18", callback_data="more_than_eighteen")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="back")

        age_keyboard = types.InlineKeyboardMarkup()
        age_keyboard.row(less_than_eighteen, more_than_eighteen)
        age_keyboard.row(back_button)

        await call.message.edit_text(text="""*First question*:
Please select your age.""", reply_markup=age_keyboard, parse_mode="Markdown")


@dp.callback_query_handler(lambda call: call.data == 'less_than_eighteen')
async def less_than_eighteen(call: types.CallbackQuery):
    name = call.from_user.full_name
    user_id = call.from_user.id
    user_language = get_user_language(user_id)

    if user_language == "ua":
        school_life = types.InlineKeyboardButton(text="📲Підключити",
                                                 url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/shkilniy/")
        not_interest = types.InlineKeyboardButton(text="❌Не цікаво", callback_data="more_than_eighteen")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="understood")

        school_life_keyboard = types.InlineKeyboardMarkup()
        school_life_keyboard.row(school_life)
        school_life_keyboard.row(not_interest)
        school_life_keyboard.row(back_button)

        await call.message.edit_text(
            text=f"*{name}*, оскільки вам менше 18-ти. Тому пропонуємо вам тариф '*Шкільний Лайф*', який зроблений спеціально для школярів.",
            parse_mode="Markdown", reply_markup=school_life_keyboard)

    if user_language == "en":
        school_life = types.InlineKeyboardButton(text="📲Connect",
                                                 url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/shkilniy/")
        not_interest = types.InlineKeyboardButton(text="❌Not interested", callback_data="more_than_eighteen")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="understood")

        school_life_keyboard = types.InlineKeyboardMarkup()
        school_life_keyboard.row(school_life)
        school_life_keyboard.row(not_interest)
        school_life_keyboard.row(back_button)

        await call.message.edit_text(
            text=f"*{name}*, because you are under 18. That's why we offer you the '*School Life*' tariff, which is specially designed for schoolchildren.",
            parse_mode="Markdown", reply_markup=school_life_keyboard)



# noinspection PyUnboundLocalVariable
@dp.callback_query_handler(lambda call: call.data == 'more_than_eighteen')
async def more_than_eighteen(call: types.CallbackQuery):
    name = call.from_user.full_name
    user_id = call.from_user.id
    user_language = get_user_language(user_id)

    if user_language == "ua":
        own_button = types.InlineKeyboardButton(text="🙋‍♂️Для себе", callback_data="for_me")
        family_button = types.InlineKeyboardButton(text="👨‍👩‍👧‍👦Для сім'ї", callback_data="for_family")
        for_gadget_button = types.InlineKeyboardButton(text="💻Для Ґаджета", callback_data="for_gadget")
        what_difference_button = types.InlineKeyboardButton(text="В чому різниця❓", callback_data="what_difference")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="understood")

        usage_select_ua = types.InlineKeyboardMarkup()
        usage_select_ua.row(own_button)
        usage_select_ua.row(family_button, for_gadget_button)
        usage_select_ua.row(what_difference_button)
        usage_select_ua.row(back_button)

        await call.message.edit_text(
            text=f"*{name}*, для якого типу використання вам потрібен тариф?", parse_mode="Markdown",
            reply_markup=usage_select_ua)

    elif user_language == "en":
        own_button = types.InlineKeyboardButton(text="🙋‍♂️For yourself", callback_data="for_me")
        family_button = types.InlineKeyboardButton(text="👨‍👩‍👧‍👦For family", callback_data="for_family")
        for_gadget_button = types.InlineKeyboardButton(text="💻For Gadget", callback_data="for_gadget")
        what_difference_button = types.InlineKeyboardButton(text="What's the difference❓",
                                                            callback_data="what_difference")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="understood")

        usage_select_en = types.InlineKeyboardMarkup()
        usage_select_en.row(own_button)
        usage_select_en.row(family_button, for_gadget_button)
        usage_select_en.row(what_difference_button)
        usage_select_en.row(back_button)

        await call.message.edit_text(
            text=f"*{name}*, for what type of use you need the tariff?", parse_mode="Markdown",
            reply_markup=usage_select_en)


@dp.callback_query_handler(lambda call: call.data == 'for_me')
async def how_much_speak(call: types.CallbackQuery):
    name = call.from_user.full_name
    user_id = call.from_user.id
    user_language = get_user_language(user_id)

    if user_language == "ua":
        sometimes_button = types.InlineKeyboardButton(text="Балакаю по необхідності", callback_data="call_sometimes")
        like_long_calls_button = types.InlineKeyboardButton(text="Частенько можу заговоритись",
                                                            callback_data="call_long_calls")
        everytime_on_phone_button = types.InlineKeyboardButton(text="Жити не можу без довгих розмов по телефону",
                                                               callback_data="call_everytime_on_phone")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="more_than_eighteen")

        calls_keyboard_ua = types.InlineKeyboardMarkup()
        calls_keyboard_ua.row(sometimes_button)
        calls_keyboard_ua.row(like_long_calls_button)
        calls_keyboard_ua.row(everytime_on_phone_button)
        calls_keyboard_ua.row(back_button)

        await call.message.edit_text(text=f"*{name}*, будьласка обери як часто ти спілкуєшся по телефону.",
                                     parse_mode="Markdown", reply_markup=calls_keyboard_ua)

    elif user_language == "en":
        sometimes_button = types.InlineKeyboardButton(text="Балакаю по необхідності", callback_data="call_sometimes")
        like_long_calls_button = types.InlineKeyboardButton(text="Частенько можу заговоритись",
                                                            callback_data="call_long_calls")
        everytime_on_phone_button = types.InlineKeyboardButton(text="Жити не можу без довгих розмов по телефону",
                                                               callback_data="call_everytime_on_phone")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="more_than_eighteen")

        calls_keyboard_en = types.InlineKeyboardMarkup()
        calls_keyboard_en.row(sometimes_button)
        calls_keyboard_en.row(like_long_calls_button)
        calls_keyboard_en.row(everytime_on_phone_button)
        calls_keyboard_en.row(back_button)

        await call.message.edit_text(text=f"*{name}*, please select how often you talk by phone.",
                                     parse_mode="Markdown", reply_markup=calls_keyboard_en)



@dp.callback_query_handler()
async def language_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    language = call.data.split('_')[1]
    await bot.send_chat_action(user_id, 'typing')
    await asyncio.sleep(0.5)

    if language == "ua":
        await call.message.edit_text(text="""Ви обрали українську мову🇺🇦!
Ви завжди можете змінити мову написавши /language
Тепер ще раз напишіть /start!
""")
        save_language_choice(user_id, language)
        await start_taryf(call.message)


    elif language == "en":
        await call.message.edit_text(text="""You have successfully selected English🇬🇧!
You can always change the language by writing /language
Now type /start again!
""")
        save_language_choice(user_id, language)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
