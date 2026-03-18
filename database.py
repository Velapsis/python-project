import sqlite3

db = sqlite3.connect("songs.db")
cursor = db.cursor()

def InitDatabase():
    with open("init.sql") as f:
        cursor.executescript(f.read())
    db.commit()

def AddHash(songId, hash):
    print("adding", hash, "to", songId)

    cursor.execute(
        """
        INSERT INTO hashs (song_id, freq1, freq2, anchor, delta)
        VALUES (?, ?, ?, ?, ?);
        """,
        (songId, hash[0], hash[1], hash[2], hash[3])
    )

    db.commit()

def SongExists(songname):
    cursor.execute("SELECT 1 FROM songs WHERE name = ?;", (songname,))
    return cursor.fetchone() is not None

def FindMatchingHashes(hash, tolerance=40):
    freq1, freq2, anchor, delta = hash
    cursor.execute(
        """
        SELECT song_id FROM hashs
        WHERE freq1 BETWEEN ? AND ?
          AND freq2 BETWEEN ? AND ?
          AND anchor BETWEEN ? AND ?
          AND delta BETWEEN ? AND ?
        """,
        (
            freq1 - tolerance, freq1 + tolerance,
            freq2 - tolerance, freq2 + tolerance,
            anchor - 40, anchor + 40,
            delta - 20, delta + 20,
        )
    )
    return [row[0] for row in cursor.fetchall()]

def GetSongName(song_id):
    cursor.execute("SELECT name FROM songs WHERE id = ?", (song_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def AddSong(songname):
    cursor.execute("SELECT id FROM songs WHERE name = ?;", (songname,))
    row = cursor.fetchone()
    if row:
        return row[0]

    cursor.execute("INSERT INTO songs (name) VALUES (?);", (songname,))
    db.commit()
    return cursor.lastrowid