#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple timer app
"""

import logging
import time
import os
import sys
import wave
from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import HermesApp
import pyaudio

_LOGGER = logging.getLogger("TimerApp")

app = HermesApp("TimerApp")
SITE_ID = "default"


def play_alarm():
    """
    Plays an alarm sound
    """
    alarm_file = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep + 'alarm.wav'
    if not os.path.exists(alarm_file):
        return
    chunk = 1024
    _file = wave.open(alarm_file, "rb")
    _audio = pyaudio.PyAudio()
    # open stream
    stream = _audio.open(
                format=_audio.get_format_from_width(_file.getsampwidth()),
                channels=_file.getnchannels(),
                rate=_file.getframerate(),
                output=True
    )
    # read data
    data = _file.readframes(chunk)
    # play stream
    while data:
        stream.write(data)
        data = _file.readframes(chunk)
    # stop stream and audio
    stream.stop_stream()
    stream.close()
    _audio.terminate()


@app.on_intent("StartTimer")
async def set_timer(intent: NluIntent):
    """
    Set the timer
    """
    unit = intent.slots[0].slot_name
    _unit = ('Sekunden' if unit == 'seconds' else 'Minuten')
    value = intent.slots[0].value['value']
    _value = (value if unit == 'seconds' else value*60)
    if value > 1:
        text = f"Okay, der Timer ist auf {value} {_unit} gestellt"
    else:
        text = f"Okay, der Timer ist auf {value} {_unit} gestellt"
    app.notify(text, SITE_ID)

    # wait and play alarm
    time.sleep(_value)
    play_alarm()
    app.notify("Deine Zeit ist abgelaufen!", SITE_ID)


app.run()