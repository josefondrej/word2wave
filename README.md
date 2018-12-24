Word2Wave
====================

Small utility to convert message in plain text to sound, that if plotted in spectral analyzer, shows the original message.
- Download some app to analyze sound spectrum to your phone (for example [Spectral Audio Analyzer](https://play.google.com/store/apps/details?id=radonsoft.net.spectralview&hl=en))
- `python -m pip install requirements.txt`
- `python w2w.py --msg "Text of your message" --play n --save y --filename "my_file.wav"`
