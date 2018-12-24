from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pyaudio
import wavio
from typing import List

class WordToWave(object):
    def __init__(self, pixel_duration: float = 0.13,
                 min_freq: float = 2000, max_freq: float = 5000, volume: float = 1.0, Fs: float = 44100,
                 channels: int = 1, silent_tone: float = 100, smoothing = 0.60,
                 img_width: float = 128, img_heigth: float = 128, font_size: int = 128,
                 start_x: int = 0, start_y: int = -24, font: str = "RobotoCondensed-Regular.ttf"):
        self._pixel_duration = pixel_duration
        self._min_freq = min_freq
        self._max_freq = max_freq
        self._volume = volume
        self._Fs = Fs

        self._samples_per_pixel = int(self._pixel_duration * self._Fs)

        self._channels = channels
        self._silent_tone = silent_tone
        self._smoothing = smoothing

        # Font properties
        self._img_width = img_width
        self._img_height = img_heigth
        self._font_size = font_size
        self._start_x = start_x
        self._start_y = start_y
        self._font = font

    def __enter__(self):
        self._p = pyaudio.PyAudio()
        self._stream = self._p.open(format=pyaudio.paFloat32,
                channels=self._channels,
                rate=self._Fs,
                output=True)
        return self

    def __exit__(self, type, value, traceback):
        self.__init__()
        self._stream.stop_stream()
        self._stream.close()
        self._p.terminate()

    def play_wave(self, wave: np.ndarray):
        for w in wave:
            self._stream.write(w.astype(np.float32).tostring())

    def save_wave(self, wave: np.ndarray, file_path: str):
        wavio.write(file_path, wave, rate = self._Fs, sampwidth = 4)

    def message_to_wave(self, message: str):
        wave = np.array([0])
        for character in message:
            wave = np.concatenate((wave, self._char_to_wave(character)))

        return wave

    def _char_to_wave(self, character: str):
        img = self._char_to_array(character)

        return self._img_to_wave(img)

    def _smooth_connect(self, a: np.ndarray, b: np.ndarray):
        smoothed_elements = int(self._smoothing * min(len(a), len(b)))
        fade = 1.0 - np.array([(i/smoothed_elements) for i in range(smoothed_elements)])
        overlap = a[-smoothed_elements:] * fade + b[0:smoothed_elements] * (1 - fade)
        smoothed_wave = np.concatenate((a[0:-smoothed_elements], overlap, b[smoothed_elements:]))
        return smoothed_wave

    def _img_to_wave(self, img: np.ndarray):
        im_ht, im_wid = img.shape

        wave = np.array([0])

        for column in range(im_wid):
            active_pixels = np.where(img[:, column])[0]
            freqs = (im_ht - active_pixels) / im_ht * (self._max_freq - self._min_freq) + self._min_freq
            if not freqs.any():
                freqs = np.array([])
            freqs = np.concatenate((freqs, np.array([self._silent_tone])))
            wave = self._smooth_connect(wave, self._composite_wave(freqs))

        return wave

    def _char_to_array(self, character: str, padding: int = 2):
        img = Image.new("L", (self._img_width, self._img_height))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self._font, self._font_size)
        draw.text((self._start_x, self._start_y), character, (255), font=font)
        img = np.asarray(img)

        # If not space, crop characters empty columns
        if np.max(img) > 0:
            non_empty = [i for i in range(self._img_width) if (img[:,i]>0).any()]
            img = img[:, non_empty]
            pad = np.zeros((self._img_height, padding))
            img = np.concatenate((pad, img, pad), axis = 1)
        else:
            img = img[:, 0:int(self._img_width/3.)]

        return img

    def _composite_wave(self, frequencies: List[float]):
        t = np.arange(self._samples_per_pixel) / self._Fs
        samples = sum([np.array([np.sin(2 * np.pi * f * t)]) for f in frequencies])
        samples = samples.reshape((-1))
        samples = self._volume * samples / np.max(np.abs(samples))

        return samples

if __name__ == "__main__":

    message = "ALPHABET"

    w2v = WordToWave()
    wave = w2v.message_to_wave(message)

    w2v.save_wave(wave, "ALPHABET.wav")

    with w2v:
        w2v.play_wave(wave)
