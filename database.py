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

def AddSong(songname):
    cursor.execute(
        """
        INSERT INTO songs (name)
        VALUES (?);
        """,
        (songname,),
    )

    db.commit()

    cursor.execute(
        "SELECT id FROM songs WHERE name = ?;",
        (songname,)
    )

    return cursor.fetchone()[0]