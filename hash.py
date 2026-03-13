import librosa
import numpy as np

# Définition du son utilisé
song = "songs/California_Dreamin.mp3"

# Load du signal audio et le sample rate à partir
audioSignal, sampleRate  = librosa.load(song)

# Généreration du spectrogram avec l'algorithme Fast Fourrier transform
spec = librosa.stft(audioSignal)

# Convertion de l'amplitude du spectogram en decibels
spec = librosa.amplitude_to_db(np.abs(spec), ref=np.max)

# Détermination du nombre de zones
zoneAmount = 30
zoneFrames = round(spec.shape[1] / zoneAmount)

# Objet zone
class Zone:
    def __init__(self, spec, start):
        self.spec = spec
        self.start = start
        
# On parcourt les zones et on slice une partie de la matrice
zones = []
for i in range(zoneAmount):
    start = i * zoneFrames
    end = (i + 1) * zoneFrames
    subspec = spec[:, start:end]
    zones.append(Zone(subspec, start))

# Pour chaque zone, on trouve le pic maximum en amplitude et on prend sa fréquence
hashs = []
for zone in zones:
    index = np.argmax(zone.spec)
    f, t = np.unravel_index(index, zone.spec.shape)
    freq = f * sampleRate / 2048
    hashs.append(freq)
    print("peak", freq, "Hz")