import sys
from word_to_wave import WordToWave

msg_limit = 50 # characters long

if len(sys.argv) < 2:
    raise ValueError("You have to type some message, e.g. `python play.py \"My message\"`")

message = sys.argv[1]

if len(message) > msg_limit:
    raise ValueError("Supports only messages shorter than %s characters" % msg_limit)

w2v = WordToWave()
print("[Converting message into wave]")
wave = w2v.message_to_wave(message)
print("\t -- done")

with w2v:
    w2v.play_wave(wave)
