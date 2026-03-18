from database import FindMatchingHashes, GetSongName

def TryMatch(recordHashs):
    votes = {}

    for hash in recordHashs:
        matching_song_ids = FindMatchingHashes(hash)
        for song_id in matching_song_ids:
            votes[song_id] = votes.get(song_id, 0) + 1

    if not votes:
        return None

    best_song_id = max(votes, key=lambda k: votes[k])
    best_score = votes[best_song_id]
    total_hashes = len(recordHashs)

    print(f"Votes: {votes}")
    print(f"Meilleur match: song_id={best_song_id} avec {best_score}/{total_hashes} hashs")

    return GetSongName(best_song_id)
