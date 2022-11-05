import io

import constants
import voice_recognizer
import image_recognizer
import settings
import converter
import keyboards
import utils

import telebot


bot = telebot.TeleBot(settings.TOKEN)


@bot.message_handler(commands=['start'])
def handler_start(message):
    bot.send_message(message.from_user.id, constants.WELCOME_MESSAGE)


@bot.message_handler(content_types=['text'])
def handler_text(message):
    """
    reply with echo msg to user text msg
    :param message: text
    :return:
    """

    bot.send_message(message.from_user.id, message.text)


@bot.message_handler(content_types=['photo'])
def photo_msg(message):
    """
    handles photo msg and reply to user with lang_keyboard
    :param message: photo
    :return:
    """

    bot.reply_to(message, constants.SELECT_IMAGE_TEXT_LANGUAGE, reply_markup=keyboards.image_keyboard())


@bot.message_handler(content_types=['voice'])
def voice_msg(message):
    """
    handles voice msg and reply to user with lang_keyboard
    :param message: voice
    :return:
    """

    bot.reply_to(message, constants.SELECT_VOICE_LANGUAGE, reply_markup=keyboards.voice_keyboard())


@bot.callback_query_handler(func=lambda call: 'image' in call.data)
def image_keyboard(call):
    """
    handles callbacks from keyboard and reply with the recognized text
    :param call: callback from image_keyboard
    :return:
    """

    image_lang = call.data.split('.')[0]
    answer = []
    for photo in call.message.reply_to_message.photo:
        tg_photo_msg = bot.get_file(photo.file_id)
        downloaded_photo = io.BytesIO(bot.download_file(tg_photo_msg.file_path))
        text_from_photo = image_recognizer.photo_2_text(downloaded_photo, image_lang)
        answer.append(utils.normalize_text(text_from_photo))

    recognized_text = ''
    if len(answer) > 1:
        for i in range(len(answer)):
            recognized_text += f"🔖Варіант {i+1}:\n{answer[i]}\n\n"

    bot.reply_to(call.message.reply_to_message, recognized_text)

    # tg_photo_msg = bot.get_file(call.message.reply_to_message.photo[1].file_id)  # downloading file (photo) # -0 +2
    # downloaded_photo = bot.download_file(tg_photo_msg.file_path)
    # jpg_file = call.message.json['reply_to_message']['photo'][1]['file_unique_id'] + '.jpg'  # -0 +2
    # open(jpg_file, 'wb').write(downloaded_photo)
    #
    # text_from_photo = image_recognizer.photo_2_text(jpg_file, image_lang)
    #
    # os.remove(jpg_file)
    #
    # bot.reply_to(call.message.reply_to_message, text_from_photo)


@bot.callback_query_handler(func=lambda call: 'voice' in call.data)
def voice_keyboard(call):
    """
    handles callbacks from keyboard and reply with the recognized speech
    :param call: callback from voice_keyboard
    :return:
    """

    voice_lang = call.data.split('.')[0]

    tg_voice_msg = bot.get_file(call.message.reply_to_message.voice.file_id)
    voice_oga = io.BytesIO(bot.download_file(tg_voice_msg.file_path))  # downloading file (voice) from telegram

    try:
        wav_file = converter.oga_2_wav_bytesio(voice_oga)  # convert .oga to .wav
    except converter.ConvertingError:
        bot.answer_callback_query(
            callback_query_id=call.id,
            cache_time=7,
            text=constants.SOMETHING_WENT_WRONG,
        )
        return

    if voice_lang == 'en':
        text_from_voice = voice_recognizer.voice_2_en(wav_file)
        bot.reply_to(call.message.reply_to_message, text_from_voice)

    elif voice_lang == 'ua':
        # text_from_voice = voice_recognizer.voice_2_ua(wav_file)
        bot.answer_callback_query(
            callback_query_id=call.id,
            cache_time=7,
            text=constants.UKRAINIAN_IS_UNAVAILABLE
        )
        # bot.reply_to(call.message.reply_to_message, text_from_voice)

    elif voice_lang == 'ru':
        text_from_voice = voice_recognizer.voice_2_ru(wav_file)
        bot.reply_to(call.message.reply_to_message, text_from_voice)


if __name__ == '__main__':
    bot.polling(none_stop=True)
