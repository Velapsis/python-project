CREATE TABLE songs(  
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    artist TEXT
);

CREATE TABLE hashs(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    song_id INTEGER,
    freq1 INTEGER,
    freq2 INTEGER,
    anchor INTEGER,
    delta INTEGER,
    FOREIGN KEY (song_id) REFERENCES songs(id)
);

CREATE INDEX hash_index
ON hashs(freq1, freq2, anchor, delta);