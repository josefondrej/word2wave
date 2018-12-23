Word2Wave
====================

Small utility to convert message in plain text to sound, that if plotted in spectral analyzer shows the original message.
Usage: Download some app to analyze sound spectra to your phone (for example Spectral Audio Analyzer).
Run `python word_to_wave.py`

To open saved file you have to use `Audacity` and `File > Import Raw` and choose `Signed 32-bit PCM`, `Little-endian`, `1-channel (Mono)`, `0`, `100`, `44100`
