from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3, secrets

DB_PATH = 'info.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_bytes(16)

def init():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Sites(id INTEGER PRIMARY KEY, name TEXT, link TEXT)')
    conn.commit()

def add_site(name, link):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('INSERT INTO Sites(name, link) VALUES(?, ?)', (name, link))
    conn.commit()

    return True

def get_sites():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('SELECT * FROM Sites')
    results = c.fetchall()

    if results:
        return results
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        link = request.form['link']
        if add_site(name, link):
            return render_template('index.html', data=get_sites())
        else:
            flash('Error Occured!')
            return render_template('index.html', data=get_sites())
    else:
        return render_template('index.html', data=get_sites())

@app.route('/delete/<id_>')
def delete_site(id_):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM Sites WHERE id = ?', (id_))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init()
    app.run(debug=True)