import copy
import random

import cv2
import telebot
import bot.constants as const
import bot.keyboards as keyboards

from bot.config import TOKEN
from bot.constants import FILE_MESSAGE, WELCOME_MESSAGE
from bot.data_structures import SetResult
from set_search import find_sets
from set_search.utils import draw_set

bot = telebot.TeleBot(TOKEN)

users_results: dict[str, SetResult] = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, WELCOME_MESSAGE)


@bot.message_handler(content_types=['document'])
def handle_file(message):
    bot.reply_to(message, FILE_MESSAGE)


@bot.message_handler(content_types=['photo'])
def handle_photo(message, ):
    photo_id = message.photo[len(message.photo) - 1].file_id
    try:
        bot.reply_to(message, 'Начал думать')
        path = bot.get_file(photo_id).file_path
        downloaded = bot.download_file(path)
        sets, image = find_sets.get_sets(downloaded)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так(' + e.__str__() + ')')
    else:
        cid = message.chat.id
        users_results[cid] = SetResult(sets, image)
        bot.send_message(cid, const.READY_MESSAGE, reply_markup=keyboards.main_menu)


@bot.message_handler(regexp=const.FORGET_IMAGE_MESSAGE)
def handle_forget_image(message):
    cid = message.chat.id
    if cid in users_results:
        del users_results[cid]
    bot.send_message(cid, const.FORGOT_MESSAGE, reply_markup=keyboards.delete_menu)


@bot.message_handler(regexp=const.HOW_MANY_SETS_MESSAGE)
def handle_how_many_sets(message):
    cid = message.chat.id
    if cid not in users_results:
        bot.send_message(cid, const.NO_IMAGE_FOUND_MESSAGE, reply_markup=keyboards.delete_menu)
        return
    current_sets = users_results[cid]
    if current_sets.has_sets:
        bot.send_message(cid, const.WHERE_IS_N_SETS_MESSAGE(len(current_sets.sets)), reply_markup=keyboards.main_menu)
    else:
        bot.send_message(cid, const.NO_SETS_MESSAGE, reply_markup=keyboards.main_menu)


@bot.message_handler(regexp=const.IS_SET_HERE_MESSAGE)
def handle_set_message(message):
    cid = message.chat.id
    if cid not in users_results:
        bot.send_message(cid, const.NO_IMAGE_FOUND_MESSAGE, reply_markup=keyboards.delete_menu)
        return
    current_sets = users_results[cid]
    if current_sets.has_sets:
        bot.send_message(cid, const.SETS_WHERE_MESSAGE, reply_markup=keyboards.main_menu)
    else:
        bot.send_message(cid, const.NO_SETS_MESSAGE, reply_markup=keyboards.main_menu)


@bot.message_handler(regexp=const.GET_HINT_MESSAGE)
def handle_hint_request(message):
    cid = message.chat.id
    if cid not in users_results:
        bot.send_message(cid, const.NO_IMAGE_FOUND_MESSAGE, reply_markup=keyboards.delete_menu)
        return
    current_sets = users_results[cid]
    if current_sets.first_unseen_set >= len(current_sets.sets):
        bot.send_message(cid, const.RUN_OUT_OF_SETS_MESSAGE, reply_markup=keyboards.main_menu)
        return
    bot.send_message(message.chat.id, const.CHOOSE_HINT_MESSAGE, reply_markup=keyboards.show_hint_menu)


@bot.message_handler(regexp=f"{const.COLOR_HINT}|{const.SHAPE_HINT}|{const.NUMBER_HINT}|{const.SHADING_HINT}")
def handle_property_hint(message):
    cid = message.chat.id
    if cid not in users_results:
        bot.send_message(cid, const.NO_IMAGE_FOUND_MESSAGE, reply_markup=keyboards.delete_menu)
        return
    current_sets = users_results[cid]
    if current_sets.first_unseen_set >= len(current_sets.sets):
        bot.send_message(cid, const.RUN_OUT_OF_SETS_MESSAGE, reply_markup=keyboards.main_menu)
        return
    value = None
    if const.SHADING_HINT == message.text:
        value = current_sets.shading[current_sets.first_unseen_set]
    elif const.COLOR_HINT == message.text:
        value = current_sets.color[current_sets.first_unseen_set]
    elif const.SHAPE_HINT == message.text:
        value = current_sets.shapes[current_sets.first_unseen_set]
    elif const.NUMBER_HINT == message.text:
        value = current_sets.amount[current_sets.first_unseen_set]
    if value is None:
        bot.send_message(cid, const.ALL_DIFFERENT_MESSAGE, reply_markup=keyboards.main_menu)
    else:
        bot.send_message(cid, const.LOOK_AT_MESSAGE(value), reply_markup=keyboards.main_menu)


@bot.message_handler(regexp=const.TYPE_HINT)
def handle_type_hint(message):
    cid = message.chat.id
    if cid not in users_results:
        bot.send_message(cid, const.NO_IMAGE_FOUND_MESSAGE, reply_markup=keyboards.delete_menu)
        return
    current_sets = users_results[cid]
    if current_sets.first_unseen_set >= len(current_sets.sets):
        bot.send_message(cid, const.RUN_OUT_OF_SETS_MESSAGE, reply_markup=keyboards.main_menu)
        return
    different = current_sets.is_different[current_sets.first_unseen_set]
    text = ""
    if different % 4 != 0:  # not 0 or 4
        if random.randint(0, 1) == 1:
            text = const.MINIMUM_ONE_PROP_DIFFERENT_MESSAGE
        elif random.randint(0, 1) == 1:
            text = const.MINIMUM_ONE_PROP_EQUAL_MESSAGE
        else:
            text = const.EQUAL_N_MESSAGE(different)
    else:
        if different == 0:
            if random.randint(0, 1) == 1:
                text = const.ALL_PROP_EQUAL_MESSAGE
            else:
                text = const.MINIMUM_ONE_PROP_EQUAL_MESSAGE
        else:
            if random.randint(0, 1) == 1:
                text = const.ALL_PROP_DIFFERENT_MESSAGE
            else:
                text = const.MINIMUM_ONE_PROP_DIFFERENT_MESSAGE

    bot.send_message(cid, text, reply_markup=keyboards.main_menu)


@bot.message_handler(regexp=f"{const.SHOW_SET_MESSAGE}|{const.NEXT_SET_MESSAGE}")
def handle_show_set(message):
    cid = message.chat.id
    if cid not in users_results:
        bot.send_message(cid, const.NO_IMAGE_FOUND_MESSAGE, reply_markup=keyboards.delete_menu)
        return
    current_sets = users_results[cid]
    if current_sets.first_unseen_set >= len(current_sets.sets):
        bot.send_message(cid, const.RUN_OUT_OF_SETS_MESSAGE, reply_markup=keyboards.main_menu)
        return
    image_with_set = draw_set(current_sets.sets[current_sets.first_unseen_set], copy.copy(current_sets.image))
    current_sets.first_unseen_set += 1
    img = cv2.imencode('.jpg', image_with_set)[1].tobytes()
    bot.send_photo(cid, img, reply_markup=keyboards.show_set_menu)


@bot.message_handler(regexp=const.BACK_MESSAGE)
def handle_back_command(message):
    cid = message.chat.id
    bot.send_message(cid, const.READY_MESSAGE, reply_markup=keyboards.main_menu)


print('Started')
bot.polling()
