import sounddevice as sd
import numpy as np

SAMPLE_RATE = 44100
DURATION = 3

print("Parle pendant 3 secondes...")
audio = sd.rec(
    frames=DURATION * SAMPLE_RATE,
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype=np.float32
)
sd.wait()

print(f"Shape : {audio.shape}")
print(f"Min : {audio.min():.4f}")
print(f"Max : {audio.max():.4f}")
print(f"Volume moyen : {np.abs(audio).mean():.4f}")

if np.abs(audio).mean() < 0.001:
    print("⚠️  Signal quasi nul — micro pas détecté ou muet")
else:
    print("✅ Micro fonctionne !")