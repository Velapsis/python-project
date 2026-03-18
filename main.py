from hash import GenerateHashs
from match import TryMatch
from database import InitDatabase, AddHash, AddSong
import sys
from pathlib import Path
from mic import record_to_file


record_to_file('test.wav')

songs_folder = Path("songs")
InitDatabase()

for song in songs_folder.iterdir():
    hashsRecord = GenerateHashs(song)
    songId = AddSong(str(song.stem))
    for hash in hashsRecord:
        AddHash(songId, hash)

# Génération des hashs




# Test des matches sur chaque son
# match = TryMatch()