#!/usr/bin/python3
# encoding: utf-8
"""
:Description: 音频转mp3
:Author: Shmily
:Create Time: 2024/11/9 10:47
:Site: shmily-qjj.top
:Deps: pip install pydub
"""

from pydub import AudioSegment


song = AudioSegment.from_wav("Python研究者.wav")

song.export("Python研究者_wav-mp3.mp3", format="mp3")

song = AudioSegment.from_ogg("Python研究者.ogg")

song.export("Python研究者_ogg-mp3.mp3", format="mp3")

AudioSegment.from_file("Python研究者.flac")

song.export("Python研究者_flac-mp3.mp3", format="mp3")