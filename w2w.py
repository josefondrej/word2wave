import sys
from word_to_wave import WordToWave
import argparse

msg_limit = 50 # characters long
default_output_file = "out.wav"

parser = argparse.ArgumentParser(description="Convert message in plain text to sound")
parser.add_argument("--msg", help="Message to be converted to sound")
parser.add_argument("--save", help="Save the converted message to a file? [Y/n]")
parser.add_argument("--play", help="Play the converted message? [y/N]")
parser.add_argument("--filename", help="Name of the file to save the converted message to. [%s]" % default_output_file)

args = parser.parse_args()



if not args.msg:
    raise ValueError("You have to type some message, e.g. `python play.py \"My message\"`")

message = args.msg

if len(message) > msg_limit:
    raise ValueError("Supports only messages shorter than %s characters" % msg_limit)

w2v = WordToWave()
print("[Converting message into wave]")
wave = w2v.message_to_wave(message)
print("\t -- done")

play = args.play and args.play.lower() == "y"
save = (not args.save) or args.save.lower() != "n"
file_path = args.filename or default_output_file

if save:
    w2v.save_wave(wave, file_path)

if play:
    with w2v:
        w2v.play_wave(wave)
