import requests
import json
import config.config as conf
from Recorder import record_audio, read_audio

# Wit speech API endpoint
API_ENDPOINT = 'https://api.wit.ai/speech'

def has_attribute(data, attribute):
    return attribute in data and data[attribute] is not None

def startRecognize(AUDIO_FILENAME, num_seconds = 5):

    # record audio of specified length in specified audio file
    record_audio(num_seconds, AUDIO_FILENAME)

    # reading audio
    audio = read_audio(AUDIO_FILENAME)

    # defining headers for HTTP request
    headers = {'authorization': conf.authorization + conf.wit_access_token,
               'Content-Type': conf.content_type
              }

    # making an HTTP post request
    resp = requests.post(API_ENDPOINT, headers = headers,
                         data = audio)

    # converting response content to JSON format
    data = json.loads(resp.content)

    if has_attribute(data, 'error'):
        print('Error: say `ok opentime` or `opentime`')
        return False

    intent = data['entities']['intent'][0]['value']
    if str(intent) == 'startAssitant':
        return True
    return False


def RecognizeSpeech(AUDIO_FILENAME, num_seconds = 5):

    # record audio of specified length in specified audio file
    record_audio(num_seconds, AUDIO_FILENAME)

    # reading audio
    audio = read_audio(AUDIO_FILENAME)

    # defining headers for HTTP request
    headers = {'authorization': conf.authorization + conf.wit_access_token,
               'Content-Type': conf.content_type
              }

    # making an HTTP post request
    resp = requests.post(API_ENDPOINT, headers = headers,
                         data = audio)

    # converting response content to JSON format
    data = json.loads(resp.content)

    # get text from data
    text = data['_text']

    # return the text
    return text, data

if __name__ == "__main__":
    while 1:
        ok = False
        while (ok == False):
            ok = startRecognize('starter.wav', 2)

        print("What can I do for you ?")
        text, data =  RecognizeSpeech('myspeech.wav', 4)
        print("\nData: {}".format(data))
        print("\nYou said: {}".format(text))
