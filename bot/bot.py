import telebot
import os

import constants
import voice_recognizer
import image_recognizer
import settings
import converter
import keyboards
import tools


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

    bot.reply_to(message, 'Вкажіть мову тексту на картинці', reply_markup=keyboards.image_keyboard())


@bot.message_handler(content_types=['voice'])
def voice_msg(message):
    """
    handles voice msg and reply to user with lang_keyboard
    :param message: voice
    :return:
    """

    bot.reply_to(message, 'Вкажіть мову голосового повідомлення', reply_markup=keyboards.voice_keyboard())


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
        downloaded_photo = bot.download_file(tg_photo_msg.file_path)
        jpg_file = photo.file_id + '.jpg'
        open(jpg_file, 'wb').write(downloaded_photo)
        text_from_photo = image_recognizer.photo_2_text(jpg_file, image_lang)
        answer.append(tools.normal_look(text_from_photo))
        os.remove(jpg_file)

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
    downloaded_voice = bot.download_file(tg_voice_msg.file_path)  # downloading file (voice) from telegram
    oga_file = call.message.json['reply_to_message']['voice']['file_unique_id'] + '.oga'
    open(oga_file, 'wb').write(downloaded_voice)  # write down voice into file (.oga)

    wav_file = converter.oga_2_wav(oga_file)  # convert .oga to .wav

    if voice_lang == 'en':
        text_from_voice = voice_recognizer.voice_2_en(wav_file)
        os.remove(oga_file)
        os.remove(wav_file)
        bot.reply_to(call.message.reply_to_message, text_from_voice)

    elif voice_lang == 'ukr':
        # text_from_voice = voice_recognizer.voice_2_ukr(wav_file)
        os.remove(oga_file)
        os.remove(wav_file)
        bot.answer_callback_query(callback_query_id=call.id, cache_time=7,
                                  text='Українська мова тимчасово недоступна :(\nВибачте за незручності.')
        # bot.reply_to(call.message.reply_to_message, text_from_voice)

    elif voice_lang == 'ru':
        text_from_voice = voice_recognizer.voice_2_ru(wav_file)
        os.remove(oga_file)
        os.remove(wav_file)
        bot.reply_to(call.message.reply_to_message, text_from_voice)


if __name__ == '__main__':
    bot.polling(none_stop=True)
