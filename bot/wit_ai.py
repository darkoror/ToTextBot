import telebot
import requests
import json
import converter
from settings import TEST_TOKEN, EN_SERVER_ACCESS_TOKEN, WIT_AI_API_ENDPOINT

bot = telebot.TeleBot(TEST_TOKEN)


@bot.message_handler(commands=['start'])
def handler_start(message):
    bot.send_message(message.chat.id, "Welcome!")


@bot.message_handler(content_types=['text'])
def handler_text(message):
    bot.send_message(message.from_user.id, message.text)


@bot.message_handler(content_types=['audio'])
def handler_audio(message):
    bot.send_message(message.from_user.id, "audio")


@bot.message_handler(content_types=['voice'])
def handler_voice(message):
    bot.send_message(message.from_user.id, "voice")

    tg_voice_msg = bot.get_file(message.voice.file_id)
    downloaded_voice = bot.download_file(tg_voice_msg.file_path)  # downloading file (voice) from telegram
    oga_file = message.json['voice']['file_unique_id'] + '.oga'
    open(oga_file, 'wb').write(downloaded_voice)  # write down voice into file (.ogg)

    wav_file = converter.oga_2_wav(oga_file)  # convert .oga to .wav

    with open(wav_file, 'rb') as f:
        audio = f.read()

    headers = {'authorization': 'Bearer ' + EN_SERVER_ACCESS_TOKEN, 'Content-Type': 'audio/wav'}
    resp = requests.post(WIT_AI_API_ENDPOINT, headers=headers, data=audio)
    data = json.loads(resp.content)
    print(data)
    text = data['_text']
    bot.send_message(message.from_user.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
