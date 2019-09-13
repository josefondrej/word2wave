Word2Wave
====================

Small utility to convert message in plain text to sound, that if plotted in spectral analyzer, shows the original message.
If you just want to see the result: 
- Download some app to analyze sound spectrum to your phone (for example [Spectral Audio Analyzer](https://play.google.com/store/apps/details?id=radonsoft.net.spectralview&hl=en))
- Play the `message.wav` file. 

If you want to generat your own messages, you have to additionally: 
- `python -m pip install requirements.txt` (I recommend using Anaconda for the pyaudio package). 
- `python w2w.py --msg "Text of your message" --play n --save y --filename "my_file.wav"`
