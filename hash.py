import librosa
import numpy as np
from scipy.ndimage import maximum_filter

def GenerateHashs(song, debug=True):
    
    # Load du signal audio et le sample rate à partir
    audioSignal, sampleRate  = librosa.load(song)
    
    # Généreration du spectrogram avec l'algorithme Fast Fourrier transform
    spec = librosa.stft(audioSignal)
    
    # Convertion de l'amplitude du spectogram en decibels (référence absolue)
    spec = librosa.amplitude_to_db(np.abs(spec), ref=1.0)
    
    # Détection de maxima locaux 2D — stable au bruit micro
    FREQ_NEIGHBORHOOD = 40   # voisinage fréquence (~860 Hz) — pics rares et saillants
    TIME_NEIGHBORHOOD = 40   # voisinage temps (~920ms)
    MIN_FREQ_HZ       = 200  # filtre DC et sub-harmoniques de bruit

    neighborhood = maximum_filter(spec, size=(FREQ_NEIGHBORHOOD, TIME_NEIGHBORHOOD))
    # Seuil = moyenne + écart-type du spectrogramme pour ne garder que les pics saillants
    threshold = spec.mean() + spec.std()
    local_max = (spec == neighborhood) & (spec > threshold)
    peak_coords = np.argwhere(local_max)  # shape (N, 2) : (freq_bin, time_frame)

    peaks = []
    for f, t in peak_coords:
        freq = int(f * sampleRate / 2048)
        if freq < MIN_FREQ_HZ:
            continue
        peaks.append((freq, int(t)))
    peaks.sort(key=lambda p: p[1])
        
    # Pour chaque pic, on génère sa paire de hashs correspondante
    # Format : (freq1, freq2, delta, anchor_time) — anchor_time utilisé pour le calcul d'offset au matching
    hashs = []
    for i in range(len(peaks)-3):
        anchor_time = int(peaks[i][1])
        hash = (int(peaks[i][0]), int(peaks[i+1][0]), int(peaks[i+1][1] - peaks[i][1]), anchor_time)
        hashs.append(hash)
        hash2 = (int(peaks[i][0]), int(peaks[i+2][0]), int(peaks[i+2][1] - peaks[i][1]), anchor_time)
        hashs.append(hash2)
        hash3 = (int(peaks[i][0]), int(peaks[i+3][0]), int(peaks[i+3][1] - peaks[i][1]), anchor_time)
        hashs.append(hash3)

    # Affichier les hashs (debug)
    if debug is True:
        for hash in hashs:
            print("hash", "(", hash[0], hash[1], hash[2], hash[3], ")")
    
    # Renvoie le tableau de hashs
    return hashs