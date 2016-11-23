#!/usr/bin/python
import time
import os
import random
import os
import json
import re
import atexit

import requests
import snowboydecoder
from memcache import Client

from creds import *
from audio_manager import AudioManager

servers = ["127.0.0.1:11211"]
mc = Client(servers, debug=1)
am = AudioManager()

def gettoken():
    token = mc.get("access_token")
    refresh = refresh_token
    if token:
        return token
    elif refresh:
        payload = {"client_id" : Client_ID, "client_secret" : Client_Secret, "refresh_token" : refresh, "grant_type" : "refresh_token", }
        url = "https://api.amazon.com/auth/o2/token"
        r = requests.post(url, data = payload)
        resp = json.loads(r.text)
        mc.set("access_token", resp['access_token'], 3570)
        return resp['access_token']
    else:
        return False


def alexa(audio_raw_data):
    url = 'https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize'
    headers = {'Authorization' : 'Bearer %s' % gettoken()}
    d = {
        "messageHeader": {
            "deviceContext": [
                {
                    "name": "playbackState",
                    "namespace": "AudioPlayer",
                    "payload": {
                        "streamId": "",
                        "offsetInMilliseconds": "0",
                        "playerActivity": "IDLE"
                    }
                }
            ]
        },
        "messageBody": {
                "profile": "alexa-close-talk",
                "locale": "en-us",
                "format": "audio/L16; rate=16000; channels=1"
        }
    }

    files = [
        ('file', ('request', json.dumps(d), 'application/json; charset=UTF-8')),
        ('file', ('audio', audio_raw_data, 'audio/L16; rate=16000; channels=1'))
    ]
    r = requests.post(url, headers=headers, files=files)
    for v in r.headers['content-type'].split(";"):
        if re.match('.*boundary.*', v):
            boundary =  v.split("=")[1]

    data = r.content.split(boundary)
    audio = None
    for d in data:
        if (len(d) >= 1024):
            audio = d.split('\r\n\r\n')[1].rstrip('--')

    if audio:
        am.play_mp3(audio)

detector = None

def detected_callback():
    print "... listening ..."
    snowboydecoder.play_audio_file()
    detector.terminate()
    raw_audio = am.get_audio()
    print "... thinking ..."
    alexa(raw_audio)

    print "Listening again..."
    wait_for_hotword()

def wait_for_hotword():
    global detector
    detector = snowboydecoder.HotwordDetector(["models/hey_alexa.pmdl", "models/alexa.pmdl"], sensitivity=0.5, audio_gain=1)
    detector.start(detected_callback)

if __name__ == "__main__":
    print('Listening... Press Ctrl+C to exit')
    wait_for_hotword()
    # detected_callback()
