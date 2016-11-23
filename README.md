# C.H.I.P Alexa Magic Mirror

## Setup

### General C.H.I.P setup

1. Flash it to use the Headless configuration.
2. Run `sudo nmtui` and configure network.
2. `sudo apt-get update`
3. `sudo apt-get upgrade`
4. `sudo apt-get install -y vim curl git gcc autoconf libtool make build-essential python-dev python-pip python-alsaaudio python-pyalsa python-pyaudio flex bison portaudio19-dev swig libasound2-dev mpg321 memcached`
5. `pip install -U pip virtualenv numpy pyaudio`


### Get Credential for Alexa Voice Service

1. http://developer.amazon.com and Goto Alexa then Alexa Voice Service
2. Create a new product type -> Device
3. Create a new security profile
    1. Under Web Settings Allow origin http://localhost:9000 and as a return URL put http://localhost:9000/code
4. Update `creds.py` with your `ProductID`, `Security_Profile_Description`, `Security_Profile_ID`, `Client_ID`, `Client_Secret`
5. Run `auth_web.py` to get the `refresh_token`


... TBD ...


## Inspired by previous works of...

* https://github.com/alexa-pi/AlexaCHIP
* https://github.com/nicholasjconn/python-alexa-voice-service
