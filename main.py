from mic import record
from mic import record_to_file
from hash import GenerateHashs
from check import TryMatch, FindBestMatch

#Enregistrement du son
record_to_file("recorded.wav")

# Génération des hashs
hashsRecord = GenerateHashs("songs/California_Dreamin.mp3")

# Test des matches sur chaque son
# match = TryMatch()