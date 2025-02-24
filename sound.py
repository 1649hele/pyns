from pydub import playback as _pupb
import pyaudio as _pd, wave as _wv, os as _os, pydub as _pu, threading as _td, librosa as _lr, soundfile as _sf, atexit as _ax, numpy as _np, io as _io, pyttsx3 as _ts
try:
    from . import func as _f, iter as _i
except ImportError:
    import func as _f, iter as _i


FILE = "dd29442deca69f52c50006b831cb216edf78a7da33748f0a80ff19f2ebe57ecd"
SR = 44100
CH = 2
FM = _pd.paInt32
FMN = _np.float32
MUSICSUFFIX = ".music"
_tts = _ts.init()


def _addexp(file, *ext):
    ext = _i.flatten(ext)
    return file + ("" if ext[0].startswith(".") else ".") + ".".join(ext) if "." not in _os.path.split(file)[-1] else file


class Sound:
    def __init__(self, file):
        self.suffix = _os.path.splitext(file)[-1]
        self.data = _io.BytesIO()
        with open(file, "rb") as f:
            self.data.write(f.read())
        self.data.seek(0)
    
    def speed_change(self, speed, file=None):
        temp = FILE if file is None else file
        temp = _addexp(temp, self.suffix)
        y, sr = _lr.load(self.data, sr=None)
        y_stretched = _lr.effects.time_stretch(y, rate=speed)
        _sf.write(temp, y_stretched, sr)
        temp = self.__class__(temp)
        return temp
    
    def play(self, cnt=1, speed=1, newthread=False, daemon=True):
        temp = self if speed == 1 else self.speed_change(speed)
        
        def play():
            _ = 0
            while _ != cnt:
                _ += 1
                _pupb.play(self.from_file())
        
        if newthread:
            _td.Thread(daemon=daemon, target=play).start()
        else:
            play()
    
    def __add__(self, other):
        temp = FILE
        a1 = self.from_file()
        a2 = other.from_file()
        t = (".mp3" if len(a1) + len(a2) > 600000 else ".wav")
        (a1 + a2).export(temp, t[1:])
        return self.__class__(temp)

    def overlay(self, other, *args, **kwargs):
        a1 = self.from_file()
        a2 = other.from_file()
        t = (".mp3" if len(a1) + len(a2) > 600000 else ".wav")
        temp = FILE
        a1.overlay(a2, *args, **kwargs).export(temp, t[1:])
        return self.__class__(temp)
    
    def __getitem__(self, item):
        a1 = self.from_file()
        temp = FILE
        a1[item].export(temp, self.suffix)
        return self.__class__(temp)

    def from_file(self):
        return _pu.AudioSegment.from_file(self.data, self.suffix)
    
    def __len__(self):
        return len(self.from_file())


def recording(st, sr=SR, channels=CH, format=FM, file=None):
    p = _pd.PyAudio()
    steam = p.open(sr, channels, format,  input=True)
    af = []
    print("\033[32mrecording start")
    for _ in range(st):
        date = steam.read(sr)
        af.append(date)
    print("recording end\033[0m")
    steam.stop_stream()
    steam.close()
    p.terminate()
    
    temp = FILE if file is None else file
    temp = _addexp(temp, ".wav")
    wav = _wv.open(temp, "wb")
    wav.setnchannels(channels)
    wav.setsampwidth(p.get_sample_size(format))
    wav.setframerate(sr)
    wav.writeframes(b"".join(af))
    wav.close()
    
    return Sound(temp)


A = 9
B = 11
C = 0
D = 2
E = 4
F = 5
G = 7
S = B + 1
K = 5
tunes = {"A": A, "B": B, "C": C, "D": D, "E": E, "F": F, "G": G}
tune = C
additionals = {"#": 1, None: 0, "b": -1}
bpm = 80


def set_tune(value):
    global tune
    if value in tunes:
        value = tunes[value]
    tune = value


def get_tune(value=None):
    if value is None:
        value = tune
    for key, value in tunes.items():
        if value == _value:
            return key


class MusicalNote:
    def __init__(self, scale, note, additional=None, beat=80):
        self.scale = scale
        self.note = note + (scale + K) * S + additionals[additional]
        self.note -= tune
        self.beat = beat
    
    def __add__(self, other):
        return self.__class__(-K, self.note + float(other) + tune, None, self.beat)
    
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return float(self) - float(other)
        else:
            return self.__class__(-K, self.note - float(other) + tune, None, self.beat)
    
    __radd__ = __add__
    
    def __rsub__(self, other):
        return self.__class__(-K, float(other) - self.note - tune, None, self.beat)
    
    def __float__(self):
        return float(self.note)
    
    def __int__(self):
        return int(self.note)
    
    def play_frequency(self):
        frequency = 440 * 2 ** ((self - A4) / 12)
        return (frequency, self.beat)


A4 = MusicalNote(0, A)


def play_music(*musicalnotes, file=None):
    musicalnotes = _i.flatten(musicalnotes)
    audio_signal = _np.array([])
    for musicalnote in musicalnotes:
        frequency, note_feet = musicalnote.play_frequency()
        note_end = SR * note_feet * 60 // bpm
        audio_signal = _np.append(audio_signal, 0.5 * _np.sin(2 * _np.pi * frequency * _np.linspace(0, note_end / SR, int(note_end), endpoint=False)))
    file = FILE if file is None else file
    file = _addexp(file, ".wav")
    audio_signal = _np.repeat(audio_signal[:, _np.newaxis], 2, axis=1)
    audio_signal = audio_signal.astype(FMN)
    wav = _wv.open(file, "wb")
    wav.setnchannels(CH)
    p = _pd.PyAudio()
    wav.setsampwidth(p.get_sample_size(FM))
    wav.setframerate(SR)
    wav.writeframes(audio_signal.tobytes())
    wav.close()
    return Sound(file)


def say(text, file=None):
    file = FILE if file is None else file
    file = _addexp(file, ".wav")
    _tts.save_to_file(text, file)
    _tts.runAndWait()
    return Sound(file)


def open_music(filename):
    pass


def _exit():
    for file in _os.listdir():
        name, exp = _os.path.splitext(file)
        if name == FILE:
            _os.remove(file)


_ax.register(_exit)
if __name__ == '__main__':
    say("你好，世界！Hello, World!").play()
