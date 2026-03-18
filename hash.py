import librosa
import numpy as np

def GenerateHashs(song, debug=True):
    
    # Load du signal audio et le sample rate à partir
    audioSignal, sampleRate  = librosa.load(song)
    
    # Généreration du spectrogram avec l'algorithme Fast Fourrier transform
    spec = librosa.stft(audioSignal)
    
    # Convertion de l'amplitude du spectogram en decibels (référence absolue)
    spec = librosa.amplitude_to_db(np.abs(spec), ref=1.0)
    
    # Détermination du nombre de zones (proportionnel à la durée)
    # hop_length=512, sr=22050 → ~43 frames/sec → FRAMES_PER_ZONE=10 ≈ 5 zones/sec
    FRAMES_PER_ZONE = 10
    zoneFrames = FRAMES_PER_ZONE
    zoneAmount = max(1, spec.shape[1] // zoneFrames)
    
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
        if subspec.size > 0:
            zones.append(Zone(subspec, start))

    # Pour chaque zone, on prend les top N pics en amplitude au-dessus du seuil
    PEAKS_PER_ZONE = 3
    AMPLITUDE_THRESHOLD_DB = -40  # en dBFS absolu — musique : -20/-30 dBFS, silence/clim : -70/-80 dBFS
    MIN_FREQ_HZ = 200              # filtre DC et sub-harmoniques de bruit (clim, etc.)
    peaks = []
    for zone in zones:
        flat = zone.spec.flatten()
        top_indices = np.argpartition(flat, -PEAKS_PER_ZONE)[-PEAKS_PER_ZONE:]
        for index in top_indices:
            if flat[index] < AMPLITUDE_THRESHOLD_DB:
                continue
            f, t = np.unravel_index(index, zone.spec.shape)
            freq = f * sampleRate / 2048
            if freq < MIN_FREQ_HZ:
                continue
            peaks.append((round(freq), t + zone.start))
    peaks.sort(key=lambda p: p[1])
        
    # Pour chaque pic, on génère sa paire de hashs correspondante
    hashs = []
    for i in range(len(peaks)-3):
        # hash(freq1, freq2, delta_t) — sans anchor absolu
        hash = (int(peaks[i][0]), int(peaks[i+1][0]), int(peaks[i+1][1] - peaks[i][1]))
        hashs.append(hash)
        hash2 = (int(peaks[i][0]), int(peaks[i+2][0]), int(peaks[i+2][1] - peaks[i][1]))
        hashs.append(hash2)
        hash3 = (int(peaks[i][0]), int(peaks[i+3][0]), int(peaks[i+3][1] - peaks[i][1]))
        hashs.append(hash3)
    
    # Affichier les hashs (debug)
    if debug is True:
        for hash in hashs:
            print("hash", "(", hash[0], hash[1], hash[2], ")")
    
    # Renvoie le tableau de hashs
    return hashs