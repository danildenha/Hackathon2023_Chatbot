import asyncio
import openai
import keep_alive

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from jsons import *

bot = Bot(token="6101040700:AAHGRNNZ1yVhNAr5cjaVEw9KFd2wrsRf3ek")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

openai.api_key = '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'


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    name = message.from_user.full_name
    user_id = message.from_user.id
    user_language = get_user_language(user_id)
    await bot.send_chat_action(user_id, 'typing')
    await asyncio.sleep(0.5)

    lang_keyboard = types.InlineKeyboardMarkup()
    lang_keyboard.add(types.InlineKeyboardButton(text="Українська🇺🇦", callback_data="lang_ua"),
                      types.InlineKeyboardButton(text="English🇬🇧", callback_data="lang_en"))

    if user_language:
        await start_taryf(message)

    else:
        await message.reply(f"""Привіт *{name}*, будь ласка обери мову!  
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
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="age_survey")

        age_keyboard = types.InlineKeyboardMarkup()
        age_keyboard.row(less_than_eighteen, more_than_eighteen)
        age_keyboard.row(back_button)

        await call.message.edit_text(text="""*Перше запитання*:
Будьласка оберіть ваш вік:""", reply_markup=age_keyboard, parse_mode="Markdown")
    elif user_language == "en":
        less_than_eighteen = types.InlineKeyboardButton(text="Below 18", callback_data="less_than_eighteen")
        more_than_eighteen = types.InlineKeyboardButton(text="Above 18", callback_data="more_than_eighteen")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="age_survey")

        age_keyboard = types.InlineKeyboardMarkup()
        age_keyboard.row(less_than_eighteen, more_than_eighteen)
        age_keyboard.row(back_button)

        await call.message.edit_text(text="""*First question*:
Please select your age:""", reply_markup=age_keyboard, parse_mode="Markdown")


@dp.callback_query_handler(lambda call: call.data == 'less_than_eighteen')
async def less_than_eighteen(call: types.CallbackQuery):
    name = call.from_user.full_name
    user_id = call.from_user.id
    user_language = get_user_language(user_id)

    if user_language == "ua":
        tariff_name = 'Шкільний Лайф'
        tariff_info = get_tariff_info(tariff_name)
        school_life = types.InlineKeyboardButton(text="📲Підключити",
                                                 url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/shkilniy/")
        not_interest = types.InlineKeyboardButton(text="❌Не цікаво", callback_data="more_than_eighteen")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="understood")

        school_life_keyboard = types.InlineKeyboardMarkup()
        school_life_keyboard.row(school_life)
        school_life_keyboard.row(not_interest)
        school_life_keyboard.row(back_button)

        await call.message.edit_text(
            text=f"""*{name}*, оскільки вам менше 18-ти, 
ми пропонуємо вам тариф '*Шкільний Лайф*', який розроблений спеціально для школярів.

Ціна: {tariff_info["Tariff price"]}
{tariff_info["Tariff internet"]}
{tariff_info["Tariff mins"]}
{tariff_info["Social bezlim"]}""",
            parse_mode="Markdown", reply_markup=school_life_keyboard)

    if user_language == "en":
        tariff_name = 'School Life'
        tariff_info = get_tariff_info_en(tariff_name)
        school_life = types.InlineKeyboardButton(text="📲Connect",
                                                 url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/shkilniy/")
        not_interest = types.InlineKeyboardButton(text="❌Not interested", callback_data="more_than_eighteen")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="understood")

        school_life_keyboard = types.InlineKeyboardMarkup()
        school_life_keyboard.row(school_life)
        school_life_keyboard.row(not_interest)
        school_life_keyboard.row(back_button)

        await call.message.edit_text(
            text=f"""*{name}*, because you are under 18, 
we offer you the '*School Life*' tariff, which is designed specifically for schoolchildren.

Price: {tariff_info["Tariff price"]}
{tariff_info["Tariff internet"]}
{tariff_info["Tariff mins"]}
{tariff_info["Social bezlim"]}""",
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
        own_button = types.InlineKeyboardButton(text="🙋‍♂️For myself", callback_data="for_me")
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


@dp.callback_query_handler(lambda call: call.data == 'what_difference')
async def what_difference_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_language = get_user_language(user_id)

    if user_language == "ua":
        back_keyboard_ua = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="more_than_eighteen")
        back_keyboard_ua.row(back_button)

        await call.message.edit_text(
            text=f"""
*Смарт Сім'я* - тариф пропонує ідеальний варіант для сімей, які бажають забезпечити доступ до зв'язку всім своїм членам. Він надає спільний пакет ресурсів, таких як хвилини розмов, повідомлення і обсяг даних, які можна використовувати для всіх номерів у сім'ї. Це дозволяє ефективно керувати витратами ресурсів і зберігати кошти, порівняно з окремими індивідуальними тарифами для кожного члена сім'ї.

*Ґаджет* - буде прекрасним варіантом для людей, які використовують багато різних пристроїв і потребують постійного доступу до Інтернету. Цей тариф зазвичай надає великий обсяг даних з високою швидкістю передачі, спеціально налаштований для потреб безперервного з'єднання.""",
            reply_markup=back_keyboard_ua, parse_mode="Markdown")

    elif user_language == "en":
        back_keyboard_en = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="more_than_eighteen")
        back_keyboard_en.row(back_button)
        await call.message.edit_text(
            text=f"""
*Smart Family* - the tariff offers an ideal option for families who want to provide access to communication to all their members. It provides a shared package of resources, such as talk minutes, messages and data, which can be used for all numbers in the family. This allows you to effectively manage resource consumption and save money compared to separate individual tariffs for each family member.

*Gadget* - is a great option for people who use many different devices and need constant access to the Internet. This tariff usually provides a large amount of data at high speeds, specially configured for the needs of a continuous connection.""",
            reply_markup=back_keyboard_en, parse_mode="Markdown")


@dp.callback_query_handler(lambda call: call.data == 'for_family')
async def for_family_handler(call: types.CallbackQuery):
    name = call.from_user.full_name
    user_id = call.from_user.id
    user_language = get_user_language(user_id)

    if user_language == "ua":
        tariff_name = "Смарт Сім'я"
        tariff_info = get_tariff_info(tariff_name)
        back_keyboard_ua = types.InlineKeyboardMarkup()
        connect = types.InlineKeyboardButton(text="📲Підключити",
                                             url="https://www.lifecell.ua/uk/mobilnij-zvyazok/smart-simya-series/")
        not_interest = types.InlineKeyboardButton(text="❌Не цікаво", callback_data="more_than_eighteen")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="more_than_eighteen")
        back_keyboard_ua.row(connect)
        back_keyboard_ua.row(not_interest)
        back_keyboard_ua.row(back_button)

        await call.message.edit_text(
            text=f"""*{tariff_name}*

Ціна: {tariff_info["Tariff price"]}
{tariff_info["Tariff internet"]}
{tariff_info["Tariff mins"]}
{tariff_info["Social bezlim"]}""",
            reply_markup=back_keyboard_ua, parse_mode="Markdown")

    elif user_language == "en":
        tariff_name = "Smart Family"
        tariff_info = get_tariff_info_en(tariff_name)
        back_keyboard_en = types.InlineKeyboardMarkup()
        connect = types.InlineKeyboardButton(text="📲Connect",
                                             url="https://www.lifecell.ua/en/mobile/smart-simya-series/")
        not_interest = types.InlineKeyboardButton(text="❌Not interested", callback_data="more_than_eighteen")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="more_than_eighteen")
        back_keyboard_en.row(connect)
        back_keyboard_en.row(not_interest)
        back_keyboard_en.row(back_button)
        await call.message.edit_text(
            text=f"""*{tariff_name}*

Price: {tariff_info["Tariff price"]}
{tariff_info["Tariff internet"]}
{tariff_info["Tariff mins"]}
{tariff_info["Social bezlim"]}""",
            reply_markup=back_keyboard_en, parse_mode="Markdown")


@dp.callback_query_handler(lambda call: call.data == 'for_gadget')
async def for_family_handler(call: types.CallbackQuery):
    name = call.from_user.full_name
    user_id = call.from_user.id
    user_language = get_user_language(user_id)

    if user_language == "ua":
        tariff_name = "Ґаджет"
        tariff_info = get_tariff_info(tariff_name)
        back_keyboard_ua = types.InlineKeyboardMarkup()
        connect = types.InlineKeyboardButton(text="📲Підключити",
                                             url="https://www.lifecell.ua/uk/mobilnij-zvyazok/gadget-series/")
        not_interest = types.InlineKeyboardButton(text="❌Не цікаво", callback_data="more_than_eighteen")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="more_than_eighteen")
        back_keyboard_ua.row(connect)
        back_keyboard_ua.row(not_interest)
        back_keyboard_ua.row(back_button)

        await call.message.edit_text(
            text=f"""*{tariff_name}*

Ціна: {tariff_info["Tariff price"]}
{tariff_info["Tariff internet"]}
{tariff_info["Tariff mins"]}
{tariff_info["Social bezlim"]}""",
            reply_markup=back_keyboard_ua, parse_mode="Markdown")

    elif user_language == "en":
        tariff_name = "Gadget"
        tariff_info = get_tariff_info_en(tariff_name)
        back_keyboard_en = types.InlineKeyboardMarkup()
        connect = types.InlineKeyboardButton(text="📲Connect",
                                             url="https://www.lifecell.ua/en/mobile/gadget-series/")
        not_interest = types.InlineKeyboardButton(text="❌Not interested", callback_data="more_than_eighteen")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="more_than_eighteen")

        back_keyboard_en.row(connect)
        back_keyboard_en.row(not_interest)
        back_keyboard_en.row(back_button)
        await call.message.edit_text(
            text=f"""*{tariff_name}*

Price: {tariff_info["Tariff price"]}
{tariff_info["Tariff internet"]}
{tariff_info["Tariff mins"]}
{tariff_info["Social bezlim"]}""",
            reply_markup=back_keyboard_en, parse_mode="Markdown")


@dp.callback_query_handler(lambda call: call.data == 'for_me')
async def budget_handler(call: types.CallbackQuery):
    name = call.from_user.full_name
    user_id = call.from_user.id
    user_language = get_user_language(user_id)

    if user_language == "ua":
        budget_button_1 = types.InlineKeyboardButton(text="до 90грн",
                                                     callback_data="budget_max-90-hrn")
        budget_button_2 = types.InlineKeyboardButton(text="100 - 170грн",
                                                     callback_data="budget_100-170-hrn")
        budget_button_3 = types.InlineKeyboardButton(text="180 - 200грн",
                                                     callback_data="budget_180-200hrn")
        budget_button_4 = types.InlineKeyboardButton(text="понад 200грн",
                                                     callback_data="budget_more-than-200-hrn")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="more_than_eighteen")

        budget_keyboard_ua = types.InlineKeyboardMarkup()
        budget_keyboard_ua.row(budget_button_1, budget_button_2)
        budget_keyboard_ua.row(budget_button_3, budget_button_4)
        budget_keyboard_ua.row(back_button)

        await call.message.edit_text(text=f"*{name}*, будь ласка обери приблизний бюджет.",
                                     parse_mode="Markdown", reply_markup=budget_keyboard_ua)

    elif user_language == "en":
        budget_button_1 = types.InlineKeyboardButton(text="up to 90 UAH",
                                                     callback_data="budget_max-90-hrn")
        budget_button_2 = types.InlineKeyboardButton(text="100 - 170 UAH",
                                                     callback_data="budget_100-170-hrn")
        budget_button_3 = types.InlineKeyboardButton(text="180 - 200 UAH",
                                                     callback_data="budget_180-200hrn")
        budget_button_4 = types.InlineKeyboardButton(text="over 200 UAH",
                                                     callback_data="budget_more-than-200-hrn")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="more_than_eighteen")

        budget_keyboard_en = types.InlineKeyboardMarkup()
        budget_keyboard_en.row(budget_button_1, budget_button_2)
        budget_keyboard_en.row(budget_button_3, budget_button_4)
        budget_keyboard_en.row(back_button)

        await call.message.edit_text(text=f"*{name}*, please select an approximate budget.",
                                     parse_mode="Markdown", reply_markup=budget_keyboard_en)


@dp.callback_query_handler(lambda call: call.data.startswith('budget_'))
async def how_much_speak(call: types.CallbackQuery):
    budget = str(call.data.split('_')[1])
    name = call.from_user.full_name
    user_id = call.from_user.id
    save_budget_choice(user_id, budget)
    user_language = get_user_language(user_id)

    if user_language == "ua":
        almost_never_button = types.InlineKeyboardButton(text="🙅‍♂️Майже ніколи(до 500хв)",
                                                         callback_data="call_max-500-min")
        sometimes_button = types.InlineKeyboardButton(text="💬Говорю при потребі(600 - 1000хв)",
                                                      callback_data="call_600-1000-min")
        like_long_calls_button = types.InlineKeyboardButton(text="🗣️Часто заговорююся(1000-2000хв)",
                                                            callback_data="call_1000-2000-min")
        everytime_on_phone_button = types.InlineKeyboardButton(text="📞Завжди на телефоні(нонад 2000хв)",
                                                               callback_data="call_over-2000-min")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="for_me")

        calls_keyboard_ua = types.InlineKeyboardMarkup()
        calls_keyboard_ua.row(almost_never_button)
        calls_keyboard_ua.row(sometimes_button)
        calls_keyboard_ua.row(like_long_calls_button)
        calls_keyboard_ua.row(everytime_on_phone_button)
        calls_keyboard_ua.row(back_button)

        await call.message.edit_text(text=f"*{name}*, будьласка обери як часто ти спілкуєшся по телефону.",
                                     parse_mode="Markdown", reply_markup=calls_keyboard_ua)

    elif user_language == "en":
        almost_never_button = types.InlineKeyboardButton(text="🙅‍♂️‍Almost never (up to 500 min)",
                                                         callback_data="call_up-to-500-min")
        sometimes_button = types.InlineKeyboardButton(text="💬I talk when needed (600-1000 min)",
                                                      callback_data="call_600-1000-min")
        like_long_calls_button = types.InlineKeyboardButton(text="🗣️I talk a lot (1000-2000 min)",
                                                            callback_data="call_1000-2000-min")
        everytime_on_phone_button = types.InlineKeyboardButton(text="📞Always on the phone (over 2000 min)",
                                                               callback_data="call_over-2000-min")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="for_me")

        calls_keyboard_en = types.InlineKeyboardMarkup()
        calls_keyboard_en.row(almost_never_button)
        calls_keyboard_en.row(sometimes_button)
        calls_keyboard_en.row(like_long_calls_button)
        calls_keyboard_en.row(everytime_on_phone_button)
        calls_keyboard_en.row(back_button)

        await call.message.edit_text(text=f"*{name}*, please select how often you talk by phone.",
                                     parse_mode="Markdown", reply_markup=calls_keyboard_en)


@dp.callback_query_handler(lambda call: call.data.startswith('call_'))
async def internet(call: types.CallbackQuery):
    phone_call = str(call.data.split('_')[1])
    name = call.from_user.full_name
    user_id = call.from_user.id
    save_calls_choice(user_id, phone_call)
    user_language = get_user_language(user_id)

    if user_language == "ua":
        mildly_internet_button = types.InlineKeyboardButton(text="💻📲Витрачаю помірно 5-10гб",
                                                            callback_data="mobdata_5-10gb")
        more_internet_button = types.InlineKeyboardButton(text="📶💾Витрачаю доволі багато 10гб+",
                                                          callback_data="mobdata_10gb+")
        everytime_online_button = types.InlineKeyboardButton(text="🌐🔥Завжди онлайн 25гб+",
                                                             callback_data="mobdata_25gb+")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="for_me")

        internet_keyboard_ua = types.InlineKeyboardMarkup()
        internet_keyboard_ua.row(mildly_internet_button)
        internet_keyboard_ua.row(more_internet_button)
        internet_keyboard_ua.row(everytime_online_button)
        internet_keyboard_ua.row(back_button)

        await call.message.edit_text(text=f"*{name}*, скільки інтернет трафіку ви використовуєте?",
                                     parse_mode="Markdown", reply_markup=internet_keyboard_ua)
    elif user_language == "en":
        mildly_internet_button = types.InlineKeyboardButton(text="💻📲I spend moderately 5-10gb",
                                                            callback_data="mobdata_5-10gb")
        more_internet_button = types.InlineKeyboardButton(text="📶💾I spend a lot 10gb+",
                                                          callback_data="mobdata_10gb+")
        everytime_online_button = types.InlineKeyboardButton(text="🌐🔥Always online 25gb+",
                                                             callback_data="mobdata_25gb+")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="for_me")

        internet_keyboard_ua = types.InlineKeyboardMarkup()
        internet_keyboard_ua.row(mildly_internet_button)
        internet_keyboard_ua.row(more_internet_button)
        internet_keyboard_ua.row(everytime_online_button)
        internet_keyboard_ua.row(back_button)

        await call.message.edit_text(text=f"*{name}*, how much internet traffic do you use?",
                                     parse_mode="Markdown", reply_markup=internet_keyboard_ua)


@dp.callback_query_handler(lambda call: call.data.startswith('mobdata_'))
async def social_handler(call: types.CallbackQuery):
    mob_data = str(call.data.split('_')[1])

    name = call.from_user.full_name
    user_id = call.from_user.id
    save_mobdata_choice(user_id, mob_data)
    user_language = get_user_language(user_id)

    if user_language == "ua":

        yes_social_button = types.InlineKeyboardButton(text="Так📱", callback_data="social_yes")
        no_social_button = types.InlineKeyboardButton(text="Ні📵",
                                                      callback_data="social_no")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="call_")

        social_keyboard_ua = types.InlineKeyboardMarkup()
        social_keyboard_ua.row(yes_social_button, no_social_button)
        social_keyboard_ua.row(back_button)

        await call.message.edit_text(text=f"*{name}*, ви вважаєте себе активним користувачем соціальних мереж?",
                                     parse_mode="Markdown", reply_markup=social_keyboard_ua)
    elif user_language == "en":

        yes_social_button = types.InlineKeyboardButton(text="Yes📱", callback_data="social_yes")
        no_social_button = types.InlineKeyboardButton(text="No📵",
                                                      callback_data="social_no")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="call_")

        social_keyboard_ua = types.InlineKeyboardMarkup()
        social_keyboard_ua.row(yes_social_button, no_social_button)
        social_keyboard_ua.row(back_button)

        await call.message.edit_text(text=f"*{name}*, do you consider yourself an active user of social media?",
                                     parse_mode="Markdown", reply_markup=social_keyboard_ua)


@dp.callback_query_handler(lambda call: call.data.startswith('social_'))
async def finish(call: types.CallbackQuery):
    social = str(call.data.split('_')[1])
    name = call.from_user.full_name
    user_id = call.from_user.id
    save_social_choice(user_id, social)
    user_language = get_user_language(user_id)

    if user_language == "ua":

        show_result_ua_button = types.InlineKeyboardButton(text="Дізнатись результат✅", callback_data="result")
        back_button = types.InlineKeyboardButton(text="⬅ Назад", callback_data="mobdata_")

        result_keyboard_ua = types.InlineKeyboardMarkup()
        result_keyboard_ua.row(show_result_ua_button)
        result_keyboard_ua.row(back_button)

        await call.message.edit_text(
            text=f"*{name}*, ви дали відповідь на всі питання, натисніть на кнопку щоб дізнатись результат!",
            parse_mode="Markdown", reply_markup=result_keyboard_ua)

    elif user_language == "en":

        show_result_ua_button = types.InlineKeyboardButton(text="Result✅", callback_data="result")
        back_button = types.InlineKeyboardButton(text="⬅ Back", callback_data="mobdata_")

        result_keyboard_ua = types.InlineKeyboardMarkup()
        result_keyboard_ua.row(show_result_ua_button)
        result_keyboard_ua.row(back_button)

        await call.message.edit_text(
            text=f"*{name}*, you have answered all questions, click on the button to find out the result!",
            parse_mode="Markdown", reply_markup=result_keyboard_ua)


@dp.callback_query_handler(lambda call: call.data.startswith('result'))
async def result(call: types.CallbackQuery):
    name = call.from_user.full_name
    user_id = call.from_user.id
    user_language = get_user_language(user_id)

    if user_language == "ua":
        await call.message.edit_text(text="Зачекайте, бот обробляє ваші відповіді!",
                                     parse_mode="Markdown")
        await bot.send_chat_action(user_id, 'typing')

        def load_tariffs():
            with open('tariffs.json', encoding='utf-8') as f:
                tariffs = json.load(f)

            restricted_tariffs = ['Шкільний Лайф', "Смарт Сім'я", 'Ґаджет']

            # Фільтруємо обмежені тарифи
            tariffs = [tariff for tariff in tariffs if tariff['Tariff name'] not in restricted_tariffs]

            return tariffs

        tariffs = load_tariffs()

        # Завантажуємо відповіді користувача з файлу JSON
        def load_user_answers():
            with open('user_answers.json', encoding='utf-8') as f:
                return json.load(f)

        user_answers = load_user_answers()

        if user_id in user_answers:
            choices = user_answers[user_id]
        else:
            choices = {}

        # Підготовка промпта
        prompt = "Оберіть найкращий тариф для користувача на основі його виборів, відповідь: найкращий тариф для користувача - назва тарифу:\n"
        prompt += "Телефонні дзвінки: {}\n".format(choices.get('phone_call', ''))
        prompt += "Мобільний інтернет: {}\n".format(choices.get('mob_data', ''))
        prompt += "Соціальні мережі: {}\n\n".format(choices.get('social', ''))
        prompt += "найменше уваги звертати на Бюджет: {}\n\n".format(choices.get('budget', ''))

        prompt += "Перелік тарифів:\n"
        for tariff in tariffs:
            tariff_info = "\nНазва: {}\nЦіна: {}\nІнтернет: {}\nДзвінки: {}\n".format(
                tariff['Tariff name'], tariff['Tariff price'], tariff['Tariff internet'], tariff['Tariff mins']
            )
            prompt += tariff_info

        # Виклик OpenAI API для отримання відповіді моделі
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=256,
            stop=None,
            temperature=1
        )

        best_tariff = response.choices[0].text.strip()

        tariff_link = None
        tariff_price = None
        tariff_internet = None
        tariff_mins = None
        tariff_bezlim = None
        back_keyboard_ua = None

        for tariff in tariffs:
            if tariff['Tariff name'] in best_tariff:
                tariff_link = tariff['Tariff href']
                tariff_price = tariff["Tariff price"]
                tariff_internet = tariff["Tariff internet"]
                tariff_mins = tariff["Tariff mins"]
                tariff_bezlim = tariff["Social bezlim"]

                break

        if tariff_link:
            back_keyboard_ua = types.InlineKeyboardMarkup()
            connect = types.InlineKeyboardButton(text="📲Підключити",
                                                 url=f"https://www.lifecell.ua/{tariff_link}")
            not_interest = types.InlineKeyboardButton(text="🌐Всі тарифи",
                                                      url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/")
            back_button = types.InlineKeyboardButton(text="🔄Обрати наново", callback_data="age_survey")
            back_keyboard_ua.row(connect)
            back_keyboard_ua.row(not_interest)
            back_keyboard_ua.row(back_button)

        await call.message.edit_text(text=f"""*{best_tariff}*

Ціна: {tariff_price}
{tariff_internet}
{tariff_mins}
{tariff_bezlim}""", parse_mode="Markdown", reply_markup=back_keyboard_ua)

    if user_language == "en":
        await call.message.edit_text(text="Wait, the bot is processing your answers!",
                                     parse_mode="Markdown")
        await bot.send_chat_action(user_id, 'typing')

        def load_tariffs():
            with open('tariffs.json', encoding='utf-8') as f:
                tariffs = json.load(f)

            restricted_tariffs = ['School Life', 'Smart Family', 'Gadget']

            # Filter the restricted tariffs
            tariffs = [tariff for tariff in tariffs if tariff['Tariff name'] not in restricted_tariffs]

            return tariffs

        tariffs = load_tariffs()

        # Load user answers from the JSON file
        def load_user_answers():
            with open('user_answers.json', encoding='utf-8') as f:
                return json.load(f)

        user_answers = load_user_answers()

        if user_id in user_answers:
            choices = user_answers[user_id]
        else:
            choices = {}

        # Preparing the prompt
        prompt = "Select the best tariff for the user based on their choices, the answer is: the best tariff for the user is the name of the tariff:\n"
        prompt += "Phone calls: {}\n".format(choices.get('phone_call', ''))
        prompt += "Mobile internet: {}\n".format(choices.get('mob_data', ''))
        prompt += "Social media: {}\n\n".format(choices.get('social', ''))
        prompt += "Least important to pay attention to Budget: {}\n\n".format(choices.get('budget', ''))

        prompt += "List of tariffs:\n"
        for tariff in tariffs:
            tariff_info = "\nName: {}\nPrice: {}\nInternet: {}\nCalls: {}\n".format(
                tariff['Tariff name'], tariff['Tariff price'], tariff['Tariff internet'], tariff['Tariff mins']
            )
            prompt += tariff_info

        # Calling the OpenAI API to get the model response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=256,
            stop=None,
            temperature=1
        )

        best_tariff = response.choices[0].text.strip()

        tariff_link = None
        tariff_price = None
        tariff_internet = None
        tariff_mins = None
        tariff_bezlim = None
        back_keyboard_en = None

        for tariff in tariffs:
            if tariff['Tariff name'] in best_tariff:
                tariff_link = tariff['Tariff href']
                tariff_price = tariff["Tariff price"]
                tariff_internet = tariff["Tariff internet"]
                tariff_mins = tariff["Tariff mins"]
                tariff_bezlim = tariff["Social bezlim"]

                break

        if tariff_link:
            back_keyboard_en = types.InlineKeyboardMarkup()
            connect = types.InlineKeyboardButton(text="📲Connect",
                                                 url=f"https://www.lifecell.ua/{tariff_link}")
            not_interest = types.InlineKeyboardButton(text="🌐All tariffs",
                                                      url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/")
            back_button = types.InlineKeyboardButton(text="🔄Choose again", callback_data="age_survey")
            back_keyboard_en.row(connect)
            back_keyboard_en.row(not_interest)
            back_keyboard_en.row(back_button)

        await call.message.edit_text(text=f"""*{best_tariff}*)

    Price: {tariff_price}
    {tariff_internet}
    {tariff_mins}
    {tariff_bezlim}""", parse_mode="Markdown", reply_markup=back_keyboard_en)


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
        await start_taryf(call.message)


if __name__ == '__main__':
    keep_alive.keep_alive()

    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
