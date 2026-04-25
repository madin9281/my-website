from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ MODEL FIRST
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

# ✅ THEN CREATE TABLE
with app.app_context():
    db.create_all()

# HOME
@app.route('/')
def home():
    return render_template('login.html')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
hashed_pwd = generate_password_hash(pwd)

new_user = User(username=user, password=hashed_pwd)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        found = User.query.filter_by(username=user).first()

if found and check_password_hash(found.password, pwd):
    return render_template('dashboard.html', username=user)
else:
    return "Wrong username or password ❌"

        if found:
            return render_template('dashboard.html', username=user)
        else:
            return "Wrong username or password ❌"

    return render_template('login.html')

if __name__ == "__main__":
    app.run()
