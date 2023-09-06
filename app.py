from flask import Flask, render_template, request, redirect, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your secret key'


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/login')


@app.route('/')
def home():
    if 'username' in session:
        return redirect('/index')
    else:
        return redirect('/login')


@app.route('/index')
def index():
    if 'username' not in session:
        flash('Please login to access this page.')
        return redirect('/login')
    con = sqlite3.connect('movies.db')
    ex = con.cursor()
    try:
        ex.execute('SELECT * FROM movies')
        movies = ex.fetchall()
        con.close()
        if len(movies) == 0:
            movies = [('http://example.com/image.png', 'No movies found', 'Please add some movies to the database', '',
                       '', '', '', '', '')]
    except sqlite3.OperationalError:
        movies = [('http://example.com/image.png', 'Table not found',
                   'Please create the movies table and add some movies to the database', '', '', '', '', '', '')]
    return render_template('index.html', len=len(movies), Movies=movies)


@app.route('/addMovie', methods=['GET'])
def add_movie_form():
    if 'username' not in session:
        flash('Please login to access this page.')
        return redirect('/login')
    return render_template('admin.html')


@app.route('/addMovie', methods=["POST"])
def add_movie():
    if 'username' not in session:
        flash('Please login to access this page.')
        return redirect('/login')
    ImageURL = request.form.get("image_url")
    title = request.form.get("title")
    plot = request.form.get("plot")
    director = request.form.get("director")
    actor1 = request.form.get("actor1")
    actor2 = request.form.get("actor2")
    actor3 = request.form.get("actor3")
    actor4 = request.form.get("actor4")
    year = request.form.get("year")

    # Check if any field is empty
    if not all([ImageURL, title, plot, director, actor1, year]):
        flash('All fields must be filled out.at least one actor ')
        return redirect('/addMovie')

    entities = (ImageURL, title, plot, director, actor1, actor2, actor3, actor4, year)
    con = sqlite3.connect('movies.db')
    ex = con.cursor()
    ex.execute(
        'CREATE TABLE IF NOT EXISTS movies(image_url text, title text, plot text, director text, actor1 text, '
        'actor2 text, actor3 text, actor4 text, year text)')
    ex.execute(
        'INSERT INTO movies(image_url, title, plot, director, actor1, actor2, actor3, actor4, year) VALUES ( ?, ?, ?, '
        '?, ?, ?, ?, ?, ?)',
        entities)
    con.commit()

    return redirect('/index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
            flash('Username and Password are required!')
            return redirect('/login')

        with sqlite3.connect('movies.db') as db:
            cursor = db.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE username = ? AND password = ?',
                (username, password,)
            )
            user = cursor.fetchone()
            if user is None:
                flash('Incorrect username or password.')
                return redirect('/login')
            else:
                session['username'] = user[0]  # store the username in session
                flash('Logged in successfully!')
                return redirect('/index')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
            flash('Username and Password are required!')
            return redirect('/signup')
        with sqlite3.connect('movies.db') as db:
            cursor = db.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS users(username text, password text)'
            )
            cursor.execute(
                'INSERT INTO users(username, password) VALUES (?, ?)',
                (username, password,)
            )
            db.commit()
            flash('Signup successful. Please login.')
            return redirect('/login')

    return render_template('signup.html')


@app.route('/movies/<title>', methods=['GET', 'POST'])
def movie_page(title):
    if 'username' not in session:
        flash('Please login to access this page.')
        return redirect('/login')
    if request.method == 'POST':
        with sqlite3.connect('movies.db') as db:
            db.execute('DELETE FROM movies WHERE title = ?', (title,))
            db.commit()
        return redirect('/index')

    with sqlite3.connect('movies.db') as con:
        ex = con.cursor()
        ex.execute('SELECT * FROM movies WHERE title = ?', (title,))
        movie_data = ex.fetchone()
    return render_template('moviepage.html', movie=movie_data)


if __name__ == '__main__':
    app.run(debug=True)
