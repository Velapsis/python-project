import librosa
import numpy as np

def GenerateHashs(song, debug=True):
    
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
    
    # Pour chaque zone, on trouve le pic maximum en amplitude et on prend sa fréquence et son instant t
    peaks = []
    for zone in zones:
        index = np.argmax(zone.spec)
        f, t = np.unravel_index(index, zone.spec.shape)
        freq, time = f * sampleRate / 2048, t + zone.start
        peaks.append((round(freq), time))
    
    # Pour chaque pic, on génère sa paire de hashs correspondante
    hashs = []
    for i in range(len(peaks)-3):
        # hash(freq1, freq2, anchor_t, delta_t)
        hash = (peaks[i][0], peaks[i+1][0], peaks[i][1], peaks[i+1][1] - peaks[i][1])
        hashs.append(hash)
        hash2 = (peaks[i][0], peaks[i+2][0], peaks[i][1], peaks[i+2][1] - peaks[i][1])
        hashs.append(hash2)
        hash3 = (peaks[i][0], peaks[i+3][0], peaks[i][1], peaks[i+3][1] - peaks[i][1])
        hashs.append(hash3)
    
    # Affichier les hashs (debug)
    if debug is True:
        for hash in hashs:
            print("hash", "(", hash[0], hash[1],  hash[2], hash[3], ")")
    
    # Renvoie le tableau de hashs
    return hashs