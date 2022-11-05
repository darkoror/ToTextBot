from bot import constants
import settings

import speech_recognition as sr


def voice_2_en(filename):
    """
    recognize english speech from voice msg
    :param filename: filename .wav
    :return: recognized speech
    """

    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
        except BaseException:
            text = constants.VOICE_TEXT_UNRECOGNIZED
    return text


def voice_2_ru(filename):
    """
    recognize russian speech from voice msg
    :param filename: filename .wav
    :return: recognized speech
    """

    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.listen(source)
        try:
            text = r.recognize_wit(audio_data=audio, key=settings.RU_SERVER_ACCESS_TOKEN)
        except BaseException:
            text = constants.VOICE_TEXT_UNRECOGNIZED
    return text


def voice_2_ua(filename):
    """
    recognize ukrainian speech from voice msg
    :param filename: filename .wav
    :return: recognized speech
    """

    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google_cloud(audio_data=audio, credentials_json="settings.CREDENTIALS", language="uk-UA")
        except BaseException as e:
            print(e)
            text = constants.VOICE_TEXT_UNRECOGNIZED
    return text
