from hash import GenerateHashs
from match import TryMatch
from database import InitDatabase, AddHash, AddSong
import sys

# Génération des hashs
hashsRecord = GenerateHashs("songs/California_Dreamin.mp3")

InitDatabase()
songId = AddSong("California_Dreamin")
for hash in hashsRecord:
    AddHash(songId, hash)

# Test des matches sur chaque son
# match = TryMatch()