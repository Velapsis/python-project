import sounddevice as sd
import numpy as np  
import soundfile as sf

SAMPLE_RATE = 44100
DURATION = 10


def record(duration=DURATION, sr=SAMPLE_RATE) -> np.ndarray:
    """Enregistre depuis le micro et retourne un array numpy float32."""
    print(f"Enregistrement {duration}s...")
    audio = sd.rec(
        frames=duration * sr,
        samplerate=sr,
        channels=1,
        dtype=np.float32
    )
    sd.wait()
    print("Terminé.")
    return audio.flatten()


def record_to_file(path: str, duration=DURATION, sr=SAMPLE_RATE):
    """Enregistre et sauvegarde en .wav."""
    audio = record(duration, sr)
    sf.write(path, audio, sr)
    return audio


def load(path: str) -> tuple[np.ndarray, int]:
    """Charge un fichier .wav. Retourne (audio, sample_rate)."""
    audio, sr = sf.read(path)
    return audio.astype(np.float32), sr


if __name__ == '__main__':
    audio = record_to_file('test.wav')
    print(f'Shape: {audio.shape}')  # (441000,)
    print(f'Min: {audio.min():.3f}, Max: {audio.max():.3f}')

