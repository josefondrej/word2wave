Word2Wave
====================

Small utility to convert message in plain text to sound, that if plotted in spectral analyzer, shows the original message.
- Download some app to analyze sound spectrum to your phone (for example [Spectral Audio Analyzer](https://play.google.com/store/apps/details?id=radonsoft.net.spectralview&hl=en))
- `python -m pip install requirements.txt`
- `python play.py "Text of your message"`

<!-- To open saved file you have to use `Audacity` and `File > Import Raw` and choose `Signed 32-bit PCM`, `Little-endian`, `1-channel (Mono)`, `0`, `100`, `44100` -->
