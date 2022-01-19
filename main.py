from set_search import utils, search, constants
import copy

import cv2 as cv

@bot.message_handler(content_types=['photo'])
def handle_photo(message, photo_id=None):
    if not photo_id:
        photo_id = message.photo[len(message.photo) - 1].file_id
    try:
        bot.reply_to(message, 'Начал думать')
        path = bot.get_file(photo_id).file_path
        downloaded = bot.download_file(path)
        imges = find_sets.get_sets(downloaded)
    except Exception as e:
        bot.reply_to(message, 'Чето не то бля(' +e.__str__())
    else:
        if len(imges) == 0:
            bot.reply_to(message, 'А рил сетов нет')
        img = cv2.imencode('.jpg', imges[random.randint(0, len(imges) - 1)])[1].tobytes()
        cid = message.chat.id
        msg = bot.send_photo(cid, img, caption='Гатова')
        photo_id = msg.photo[len(msg.photo) - 1].file_id



print('Started')
bot.polling()
