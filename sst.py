import config.config as conf
import json
import requests
import time
from Recorder import record_audio, read_audio

# Wit speech API endpoint
API_ENDPOINT = 'https://api.wit.ai/speech'

def has_attribute(data, attribute):
    return attribute in data and data[attribute] is not None

def command_error():
    print ("Unavailable command")

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

    if has_attribute(data['entities'], 'intent'):
        intent = data['entities']['intent'][0]['value']
        if str(intent) == 'startAssitant':
            return True
    return False


def RecognizeSpeech(AUDIO_FILENAME, num_seconds = 5):
    start_time = time.time()
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

    excTime = round(time.time() - start_time, 2)
    # return the text
    return data, excTime

if __name__ == "__main__":
    while 1:
        ok = False
        while (ok == False):
            ok = startRecognize('starter.wav', 2)

        print("What can I do for you ?")

        data, excTime =  RecognizeSpeech('myspeech.wav', 4)
        print("\nData: {}".format(data))

        if has_attribute(data, '_text'):
            print("\nYou said: {}".format(data['_text']))
        url = "http://api.opentime.com/"

        if has_attribute(data, 'entities'):
            if has_attribute(data['entities'], 'intent'):
                ressource = data['entities']['intent'][0]['value']
                url += ressource + '/'
            else:
                command_error()

            if has_attribute(data['entities'], 'contact'):
                contact = data['entities']['contact'][0]['value']
                url += contact
        print('API call: `%s`' % url)

        print("\nTime: %s seconds" % excTime)
