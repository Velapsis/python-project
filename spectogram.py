import librosa
import numpy as np
import matplotlib.pyplot as plt

def SpectogramGen(song, show=False):
    # Load du signal audio et le sample rate à partir
    audioSignal, sampleRate  = librosa.load(song, sr=None)

    # Généreration du spectrogram avec l'algorithme Fast Fourrier transform
    spec = librosa.stft(audioSignal)
    
    # Convertion de l'amplitude du spectogram en decibels
    spec = librosa.amplitude_to_db(np.abs(spec), ref=np.max)
    
    # Génération du graphique du spectogramme avec pyplot si show = True
    if (show is True):
        plt.figure()
        librosa.display.specshow(spec)
        plt.colorbar()
        plt.title("Spectre audio " + str(sampleRate) + " Hz")
        plt.show()
    else:
        return spec