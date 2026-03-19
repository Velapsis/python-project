from collections import defaultdict
from database import FindMatchingHashes, GetSongName

def TryMatch(recordHashs):
    # Vote sur (song_id, offset) — offset = temps_dans_song - temps_dans_recording
    # Une vraie match aura beaucoup de hashs avec le même offset
    offsets = defaultdict(int)

    for hash in recordHashs:
        rec_time = hash[3]
        matches = FindMatchingHashes(hash)
        for song_id, song_time in matches:
            offset = (song_time - rec_time) // 5 * 5  # bin de 5 frames (~115ms) pour absorber le jitter micro
            offsets[(song_id, offset)] += 1

    if not offsets:
        return None

    best = max(offsets, key=offsets.get)
    best_song_id, best_offset = best
    best_score = offsets[best]
    total_hashes = len(recordHashs)

    top5 = sorted(offsets.items(), key=lambda x: x[1], reverse=True)[:5]
    for (sid, off), votes in top5:
        print(f"  song_id={sid}, offset={off}, votes={votes}")
    print(f"Meilleur match: song_id={best_song_id}, offset={best_offset}, votes={best_score}/{total_hashes}")

    return GetSongName(best_song_id)
