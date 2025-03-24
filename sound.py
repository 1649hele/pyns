from pydub import playback
import pyaudio, wave, os, pydub, librosa, soundfile, atexit, numpy, io, pyttsx3
try:
    from . import func, iter, file
except ImportError:
    import func, iter, file


SR = 44100
CH = 2
FM = pyaudio.paInt32
FMN = numpy.float32
MUSICSUFFIX = ".music"
_tts = pyttsx3.init()


def _addexp(file, *ext):
    ext = iter.flatten(ext)
    return file + ("" if ext[0].startswith(".") else ".") + ".".join(ext) if "." not in os.path.split(file)[-1] else file


class Sound:
    def __init__(self, file):
        self.suffix = os.path.splitext(file)[-1]
        self.data = io.BytesIO()
        with open(file, "rb") as f:
            self.data.write(f.read())
        self.data.seek(0)
    
    def speed_change(self, speed, file=None):
        temp = file.get_random_filename() if file is None else file
        temp = _addexp(temp, self.suffix)
        y, sr = librosa.load(self.data, sr=None)
        y_stretched = librosa.effects.time_stretch(y, rate=speed)
        soundfile.write(temp, y_stretched, sr)
        temp = self.__class__(temp)
        return temp
    
    def play(self, cnt=1, speed=1, newthread=False, daemon=True):
        temp = self if speed == 1 else self.speed_change(speed)
        
        def play():
            _ = 0
            while _ != cnt:
                _ += 1
                plaeyback.play(self.from_file())
        
        if newthread:
            threading.Thread(daemon=daemon, target=play).start()
        else:
            play()
    
    def __add__(self, other):
        temp = file.get_random_filename()
        a1 = self.from_file()
        a2 = other.from_file()
        t = (".mp3" if len(a1) + len(a2) > 600000 else ".wav")
        (a1 + a2).export(temp, t[1:])
        return self.__class__(temp)

    def overlay(self, other, *args, **kwargs):
        a1 = self.from_file()
        a2 = other.from_file()
        t = (".mp3" if len(a1) + len(a2) > 600000 else ".wav")
        temp = file.get_random_filename()
        a1.overlay(a2, *args, **kwargs).export(temp, t[1:])
        return self.__class__(temp)
    
    def __getitem__(self, item):
        a1 = self.from_file()
        temp = file.get_random_filename()
        a1[item].export(temp, self.suffix)
        return self.__class__(temp)

    def from_file(self):
        return pudub.AudioSegment.from_file(self.data, self.suffix)
    
    def __len__(self):
        return len(self.from_file())


def recording(st, sr=SR, channels=CH, format=FM, file=None):
    p = pyaudio.PyAudio()
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
    
    temp = file.get_random_filename() if file is None else file
    temp = _addexp(temp, ".wav")
    wav = wave.open(temp, "wb")
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
    musicalnotes = iter.flatten(musicalnotes)
    audio_signal = numpy.array([])
    for musicalnote in musicalnotes:
        frequency, note_feet = musicalnote.play_frequency()
        note_end = SR * note_feet * 60 // bpm
        audio_signal = numpy.append(audio_signal, 0.5 * numpy.sin(2 * numpy.pi * frequency * numpy.linspace(0, note_end / SR, int(note_end), endpoint=False)))
    file = file.get_random_filename() if file is None else file
    file = _addexp(file, ".wav")
    audio_signal = numpy.repeat(audio_signal[:, numpy.newaxis], 2, axis=1)
    audio_signal = audio_signal.astype(FMN)
    wav = wave.open(file, "wb")
    wav.setnchannels(CH)
    p = pyaudio.PyAudio()
    wav.setsampwidth(p.get_sample_size(FM))
    wav.setframerate(SR)
    wav.writeframes(audio_signal.tobytes())
    wav.close()
    return Sound(file)


def say(text, file=None):
    file = file.get_random_filename() if file is None else file
    file = _addexp(file, ".wav")
    _tts.save_to_file(text, file)
    _tts.runAndWait()
    return Sound(file)


def open_music(filename):
    pass


def _exit():
    for file in os.listdir():
        name, exp = os.path.splitext(file)
        if name == file.get_random_filename():
            os.remove(file)


atexit.register(_exit)
if __name__ == '__main__':
    say("你好，世界！Hello, World!").play()
