import sqlite3
import pandas as pd
from flask import Flask, render_template, request, session, redirect, jsonify, url_for
from datetime import timedelta

app = Flask(__name__, template_folder="Templates/", static_folder="Static/")
app.secret_key = '123456'


# app.permanent_session_lifetime = timedelte(days=2)


def get_db():
    conn = sqlite3.connect("eurovision.db")
    conn.row_factory = sqlite3.Row
    return conn


def close_db(conn):
    if conn:
        conn.close()


@app.cli.command('initdb')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print('Initialized the database.')


@app.route('/')
def landing_page():
    return render_template('start.html')


@app.route("/login", methods=["GET", "POST"])
def login():

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        username = request.form["username"]
        cursor.execute("SELECT user_id, user_name FROM users WHERE user_name = ?", (username,))
        user = cursor.fetchone()

        if user:
            session["user_id"] = user["user_id"]
            session["user"] = user["user_name"]
            return redirect("/get_score")

        else:
            # Create a new user if the username doesn't exist
            try:
                cursor.execute("INSERT INTO users (user_name) VALUES (?)", (username,))
                conn.commit()
                # Get the ID of the newly inserted user
                cursor.execute("SELECT last_insert_rowid()")
                user_id = cursor.fetchone()[0]
                session["user_id"] = user_id
                session["user"] = username
                return redirect("get_score")

            except sqlite3.Error as e:
                conn.rollback()
                conn.close()
                return f"Error creating user: {e}", 500


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return "logged out"


@app.route("/get_score", methods=['GET', 'POST'])
def get_score():

    all_songs = []
    scored_song_ids = set()
    available_songs = []

    conn = get_db()
    cursor = conn.cursor()

    user_id = session.get("user_id")

    try:
        cursor.execute("SELECT * FROM songs")
        all_songs = cursor.fetchall()
        print(all_songs)

        if user_id:
            cursor.execute("SELECT song_id FROM scoring WHERE user_id = ?", (user_id,))
            scored_songs_rows = cursor.fetchall()
            scored_song_ids = {row['song_id'] for row in scored_songs_rows}

            available_songs = [song for song in all_songs if song['song_id'] not in scored_song_ids]

    except sqlite3.Error as e:
        print(f"Error fetching songs or scored songs: {e}")

    if request.method == "POST":

        comment = request.form["comment"]
        song_score = request.form["song_score"]
        perf_score = request.form["perf_score"]
        song_id = request.form["song_id"]

        if not all([song_score, perf_score, song_id]):
            print("Please fill in all but the comment field.")
        else:
            if user_id:
                try:
                    if song_id in scored_song_ids:
                        print("You have already scored this song.")
                    else:
                        cursor.execute("""
                              INSERT INTO scoring (song_id, user_id,  song_comment, song_score1, perf_score1)
                              VALUES (?, ?, ?, ?, ?)""", (song_id, user_id,  comment, song_score, perf_score))
                        conn.commit()

                        available_songs = [song for song in available_songs if song['song_id'] != int(song_id)]

                except sqlite3.Error as e:
                    conn.rollback()
                    close_db(conn)
                    return f"Error inserting data: {e}"
            else:
                close_db(conn)
                return "User not logged in", 401

    if conn:
        close_db(conn)
    return render_template("index.html", songs=available_songs)


@app.route("/second", methods=["GET", "POST"])
def get_second():

    user_id = session.get("user_id")

    if user_id:

        df = pd.read_sql_query(con=get_db(),
                               sql=f"""SELECT users.user_id, users.user_name, songs.song_country, songs.song_name, songs.song_artist, 
                               scoring.song_score1, scoring.perf_score1, scoring.song_comment
                                FROM
                                    scoring
                                JOIN
                                    users ON scoring.user_id = users.user_id
                                JOIN
                                    songs ON scoring.song_id = songs.song_id;""")

        df = df.rename(columns={"user_id": "ID", "user_name": "Name", "song_country": "Land",
                                "song_name": "Song Name", "song_artist": "Künstler",  "song_score1": "Song Score",
                                "perf_score1": "Performance Score", "song_comment": "Kommentar"})

        df = df.sort_values(by="Land")
        user_df = df.query(f"ID == {user_id}")

        table = user_df.to_html(index=False)
        user_df.to_html("result1.html", index=False)

        return table

    if request.method == "POST":

        comment = request.form["comment"]
        song_score = request.form["song_score"]
        perf_score = request.form["perf_score"]

        conn = get_db()
        cursor = conn.cursor()

        if "user_id" in session:
            user_id = session["user_id"]

            try:
                cursor.execute("""INSERT INTO scoring (user_id, song_id, song_comment, song_score2, perf_score2) 
                VALUES (?,?,?,?,?)""", (user_id, song_id, comment, song_score, perf_score))
                conn.commit()
                close_db(conn)
                return render_template("index.html", songs=songs)

            except sqlite3.Error as e:
                conn.rollback()
                close_db(conn)
                return f"Error inserting data: {e}"


# @app.route("/result", methods=["GET", "POST"])
# def get_secod():
#     if "user" in session:
#         name = session["user"]
#         df = pd.read_sql_query(con=get_db(), sql=f""" SELECT * FROM songs
#         WHERE user_name='{name}';""")
#         result = df.to_html()
#         return result


# def get_data():
#     print(table)


if __name__ == "__main__":
    app.run(debug=True, host="192.168.2.221", port=5000)

# cursor.execute("""INSERT INTO scoring (song_id, user_id, song_comment, song_score1, perf_score1)
# VALUES (?,?,?,?,?)""", (song_id, user_id, comment, song_score, perf_score))
# conn.commit()
# return render_template("index.html", songs=songs)
