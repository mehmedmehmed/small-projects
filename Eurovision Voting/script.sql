SELECT
    users.user_name,
    songs.song_country,
    scoring.song_score1,
    scoring.perf_score1,
    scoring.song_comment
FROM
    scoring
JOIN
    users ON scoring.user_id = users.user_id
JOIN
    songs ON scoring.song_id = songs.song_id;