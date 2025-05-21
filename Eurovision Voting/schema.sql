DROP TABLE IF EXISTS songs;

CREATE TABLE songs (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_country TEXT,
    song_name TEXT,
    song_artist TEXT
    );

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT UNIQUE NOT NULL
    );

DROP TABLE IF EXISTS scoring;

CREATE TABLE scoring (
    song_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    song_comment TEXT,
    song_score1 INTEGER,
    song_score2 INTEGER,
    perf_score1 INTEGER,
    perf_score2 INTEGER,
    PRIMARY KEY (user_id, song_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

