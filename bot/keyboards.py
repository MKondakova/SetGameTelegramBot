import telebot

import bot.constants as const

back_btn = telebot.types.KeyboardButton(const.BACK_MESSAGE)

main_menu = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)

main_menu_btn_1 = telebot.types.KeyboardButton(const.IS_SET_HERE_MESSAGE)
main_menu_btn_2 = telebot.types.KeyboardButton(const.HOW_MANY_SETS_MESSAGE)
main_menu_btn_3 = telebot.types.KeyboardButton(const.SHOW_SET_MESSAGE)
main_menu_btn_4 = telebot.types.KeyboardButton(const.GET_HINT_MESSAGE)
main_menu_btn_5 = telebot.types.KeyboardButton(const.FORGET_IMAGE_MESSAGE)
main_menu.add(main_menu_btn_1, main_menu_btn_2, main_menu_btn_3, main_menu_btn_4, main_menu_btn_5)

show_set_menu = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)

show_set_menu_btn_1 = telebot.types.KeyboardButton(const.NEXT_SET_MESSAGE)
show_set_menu.add(show_set_menu_btn_1, back_btn)

show_hint_menu = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=3)
show_hint_menu_btn_1 = telebot.types.KeyboardButton(const.COLOR_HINT)
show_hint_menu_btn_2 = telebot.types.KeyboardButton(const.SHAPE_HINT)
show_hint_menu_btn_3 = telebot.types.KeyboardButton(const.SHADING_HINT)
show_hint_menu_btn_4 = telebot.types.KeyboardButton(const.NUMBER_HINT)
show_hint_menu_btn_5 = telebot.types.KeyboardButton(const.TYPE_HINT)
show_hint_menu.add(show_hint_menu_btn_1, show_hint_menu_btn_2, show_hint_menu_btn_3, show_hint_menu_btn_4,
                   show_hint_menu_btn_5, back_btn)

delete_menu = telebot.types.ReplyKeyboardRemove()
