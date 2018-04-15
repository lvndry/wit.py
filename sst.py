import config.config as conf
import json
import os
import platform
import requests
import sys
import time
from Recorder import record_audio, read_audio

# Wit speech API endpoint
WIT_API_ENDPOINT = 'https://api.wit.ai/speech'


def has_attribute(data, attribute):
    return attribute in data and data[attribute] is not None


def command_error():
    print("Error: Wit.ai doesn't understand this command")


def isWavFile(path):
    return os.path.exists(path) is not False


def startRecognize(AUDIO_FILENAME, num_seconds=5):

    # record audio of specified length in specified audio file
    wav_record = record_audio(num_seconds, AUDIO_FILENAME)

    if wav_record == False:
        print("Sorry can't understand what you said")
        return False

    # reading audio
    audio = read_audio(AUDIO_FILENAME)

    # defining headers for HTTP request
    headers = {'authorization': conf.authorization + conf.wit_access_token,
               'Content-Type': conf.content_type
               }

    start_request = time.time()
    # making an HTTP post request
    resp = requests.post(WIT_API_ENDPOINT, headers=headers,
                         data=audio)
    request_time = round(time.time() - start_request, 2)
    print('Request: ' + str(request_time) + 's')

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


def RecognizeSpeech(AUDIO_FILENAME, num_seconds=5, live=True):
    start_time = time.time()
    # record audio of specified length in specified audio file
    if live == True:
        wav_record = record_audio(num_seconds, AUDIO_FILENAME)

        if wav_record == False:
            print("Sorry can't understand what you said")
            return False

    # reading audio
    audio = read_audio(AUDIO_FILENAME)

    # defining headers for HTTP request
    headers = {'authorization': conf.authorization + conf.wit_access_token,
               'Content-Type': conf.content_type,
               }

    start_request = time.time()
    # making an HTTP post request
    resp = requests.post(WIT_API_ENDPOINT, headers=headers,
                         data=audio)
    request_time = round(time.time() - start_request, 2)
    print('Request ' + str(request_time) + 's')

    # converting response content to JSON format
    data = json.loads(resp.content)

    excTime = round(time.time() - start_time, 2)

    return data, excTime


def build_URL(data):
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
    return url


if __name__ == "__main__":
    print("Opentime vocal assistant\n")

    if len(sys.argv) > 1:
        print('Start analyzing wav file...')
        if platform.system() == 'Windows':
            path = os.getcwd() + '\\' + sys.argv[1]
        else:
            path = os.getcwd() + '/' + sys.argv[1]
        print('Path: ' + path)

        if isWavFile(path):
            data, excTime = RecognizeSpeech(path, 4, False)

            if has_attribute(data, 'error') or False:
                command_error()
            else:
                url = build_URL(data)
                print('\nAPI call: `%s`' % url)
                print("\nTime: %s seconds" % excTime)
        else:
            print('Make sure this is the good path to the wav file')
    else:
        while 1:
            trigger = False
            while (trigger == False):
                trigger = startRecognize('starter.wav', 1.6)

            print("What can I do for you ?")

            data, excTime = RecognizeSpeech('myspeech.wav', 4)
            print("\nData: {}".format(data))

            if has_attribute(data, 'error') or False:
                command_error()
            else:
                url = build_URL(data)
                print('\nAPI call: `%s`' % url)
                print("\nTime: %s seconds" % excTime)
