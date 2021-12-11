from flask import Flask, render_template, url_for, request, flash, redirect, session, jsonify
import cs304dbi as dbi
import random, bcrypt, json

app = Flask(__name__)
app.secret_key = "hello"

dbi.conf(db='lect_db')
conn = dbi.connect()
curs = dbi.cursor(conn)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/set-UID', methods=['POST'])
def setUID():
    uid = request.form['uid']
    curs.execute("SELECT uid FROM staff WHERE uid = %s;", [uid])
    data = curs.fetchone()
    session['uid'] = data[0]
    return redirect(url_for('showAllMovies', uid=data[0]))

@app.route('/show-all-movies')
def showAllMovies():
    data = request.args['uid']
    curs.execute('select * from movie')
    movies = curs.fetchall()
    return render_template('show-all-movies.html', uid = data, movies = movies)

@app.route('/rate-one-movie', methods=['POST'])
def rateOneMovie():
    data = request.form['rating']
    print(data)
    data = data.replace("\'", "\"")
    data = json.loads(data)

    rating = data['rating']
    uid = data['uid']
    tt = data['tt']

    curs.execute('''
                INSERT INTO individualRating (tt, uid, rating) 
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY
                    UPDATE tt = VALUES(tt), uid = VALUES(uid), rating = VALUES(rating);
                ''', [tt, uid, rating])
    conn.commit()

    curs.execute('SELECT AVG(rating) FROM individualRating WHERE tt = %s', [tt])
    newRating = curs.fetchone()[0]

    curs.execute('''
                UPDATE movie 
                SET avgRating = %s
                WHERE tt = %s;
                ''', [newRating, tt])
    conn.commit()

    flash(f"User {uid} is rating the movie tt {tt} as {rating} stars. New average is {newRating}")
    return redirect(url_for('showAllMovies', uid=uid))

@app.route('/rate-one-movie-ajax/', methods=['POST'])
def rateMovieAjax():
    data = request.form['data']
    data = data.replace("\'", "\"")
    data = json.loads(data)
    

    rating = data['rating']
    uid = data['uid']
    tt = data['tt']

    curs.execute('''
                INSERT INTO individualRating (tt, uid, rating) 
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY
                    UPDATE tt = VALUES(tt), uid = VALUES(uid), rating = VALUES(rating);
                ''', [tt, uid, rating])
    conn.commit()

    curs.execute('SELECT AVG(rating) FROM individualRating WHERE tt = %s', [tt])
    newRating = curs.fetchone()[0]

    curs.execute('''
                UPDATE movie 
                SET avgRating = %s
                WHERE tt = %s;
                ''', [newRating, tt])
    conn.commit()

    response = {'avgRating': newRating}

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=8002)