import speech_recognition as sr
import settings


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
        except:
            text = 'На жаль, мені не вдалося розпізнати те, що Ви сказали :('
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
            text = r.recognize_wit(audio_data=audio, key='BTSXQDFI5VXYM575B7UKNT65DLETMFW6')
        except:
            text = 'На жаль, мені не вдалося розпізнати те, що Ви сказали :('
    return text


def voice_2_ukr(filename):
    """
    recognize ukrainian speech from voice msg
    :param filename: filename .wav
    :return: recognized speech
    """

    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google_cloud(audio_data=audio, credentials_json=settings.CREDENTIALS, language="uk-UA")
        except BaseException as e:
            print(e)
            text = 'На жаль, мені не вдалося розпізнати те, що Ви сказали :('
    return text
