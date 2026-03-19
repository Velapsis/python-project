from init import setup
setup()

from hash import GenerateHashs
from match import TryMatch
from database import InitDatabase, AddHash, AddSong
from pathlib import Path
from mic import record_to_file
import sys

match_only = '--match-only' in sys.argv


InitDatabase()

# Indexer les songs dans la DB (skip si déjà présente)
from database import SongExists
songs_folder = Path("songs")
for song in songs_folder.iterdir():
    if not SongExists(str(song.stem)):
        print(f"Indexing {song.stem}...")
        songId = AddSong(str(song.stem))
        hashsRecord = GenerateHashs(song)
        for hash in hashsRecord:
            AddHash(songId, hash)
    else:
        print(f"Skip {song.stem} (déjà indexée)")

# Enregistrer depuis le micro
if not match_only:
    record_to_file('test.wav')

# Hasher le recording et trouver le match
recordHashs = GenerateHashs('test.wav')
result = TryMatch(recordHashs)

if result:
    print(f"\n>>> Song reconnue : {result}")
else:
    print("\n>>> Aucun match trouvé")
