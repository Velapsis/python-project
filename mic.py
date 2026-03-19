import sounddevice as sd
import numpy as np  
import soundfile as sf

SAMPLE_RATE = 44100
DURATION = 10


def record(duration=DURATION, sr=SAMPLE_RATE) -> np.ndarray:
    """Enregistre depuis le micro et retourne un array numpy float32."""
    print(f"Enregistrement {duration}s...")
    audio = sd.rec(
        frames=duration * sr,  # ← frames pas frame
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


# def load(path: str) -> tuple[np.ndarray, int]:
#     """Charge un fichier .wav. Retourne (audio, sample_rate)."""
#     audio, sr = sf.read(path)
#     return audio.astype(np.float32), sr


# def test_mic(duration=3, sr=SAMPLE_RATE):
#     """Teste rapidement si le micro fonctionne."""
#     print("Test micro — parle pendant 3 secondes...")
#     audio = record(duration, sr)
#     print(f"Shape : {audio.shape}")
#     print(f"Min : {audio.min():.4f} | Max : {audio.max():.4f}")
#     print(f"Volume moyen : {np.abs(audio).mean():.4f}")
#     if np.abs(audio).mean() < 0.001:
#         print("⚠️  Signal quasi nul — micro muet ou mauvais device")
#         print("Devices disponibles :")
#         print(sd.query_devices())
#     else:
#         print("✅ Micro OK !")


# if __name__ == '__main__':
#     import sys
#     if len(sys.argv) > 1 and sys.argv[1] == '--test':
#         test_mic()
#     else:
#         audio = record_to_file('test.wav')
#         print(f'Shape: {audio.shape}')
#         print(f'Min: {audio.min():.3f}, Max: {audio.max():.3f}')