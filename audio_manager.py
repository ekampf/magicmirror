import pyaudio
import wave
import subprocess
import speech_recognition
import time
import os

class AudioManager(object):
    def get_audio(self, timeout=0):
        r = speech_recognition.Recognizer()

        with speech_recognition.Microphone() as source:
            if not timeout:
                print "What do you want?"
                audio = r.listen(source)
            else:
                print "What do you want? (%s seconds)" % timeout
                try:
                    audio = r.listen(source, timeout=timeout)
                except speech_recognition.WaitTimeoutError:
                    return None

        with open("tmp/microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())

        # Convert audio to raw_data (PCM)
        raw_audio = audio.get_raw_data()
        return raw_audio

    def play_mp3(self, raw_audio):
        # Save MP3 data to a file
        with open("tmp/response.mp3", 'wb') as f:
            f.write(raw_audio)

        # Convert mp3 response to wave (pyaudio doesn't work with MP3 files)
        subprocess.Popen(['ffmpeg', '-y', '-i', 'tmp/response.mp3', 'tmp/response.wav'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()

        # Play a wave file directly
        self.play_wav('tmp/response.wav')

    def play_wav(self, file, timeout=None, stop_event=None, repeat=False):
        """ Play a wave file using PyAudio. The file must be specified as a path.

        :param file: path to wave file
        """
        p = pyaudio.PyAudio()
        # Open wave wave
        wf = wave.open(file, 'rb')
        # Create pyaudio stream
        stream = p.open(
                    format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

        # Set chunk size for playback
        chunk = 1024

        # Get start time
        start_time = time.mktime(time.gmtime())

        end = False
        while not end:
            # Read first chunk of data
            data = wf.readframes(chunk)
            # Continue until there is no data left
            while len(data) > 0 and not end:
                if timeout is not None and time.mktime(time.gmtime())-start_time > timeout:
                    end = True
                if stop_event is not None and stop_event.is_set():
                    end = True
                stream.write(data)
                data = wf.readframes(chunk)
            if not repeat:
                end = True
            else:
                wf.rewind()

        # When done, stop stream and close
        stream.stop_stream()
        stream.close()
        wf.close()

        p.terminate()
