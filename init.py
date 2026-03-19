import sys
import os
import subprocess

VENV_DIR = os.path.join(os.path.dirname(__file__), "venv")
DEPENDENCIES = ["librosa", "numpy", "scipy", "sounddevice", "soundfile"]

def setup():
    # Si on n'est pas dans un venv, en créer un et relancer le script dedans
    if sys.prefix == sys.base_prefix:
        if not os.path.exists(VENV_DIR):
            print("Création du venv...")
            subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)

        venv_python = os.path.join(VENV_DIR, "bin", "python")
        print("Activation du venv et relancement...")
        os.execv(venv_python, [venv_python] + sys.argv)

    # Dans le venv — installer les dépendances manquantes
    print("Vérification des dépendances...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "--upgrade", *DEPENDENCIES],
        check=True
    )
    print("Dépendances OK.")
