from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

# Database Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

@app.route('/')
def home():
    return render_template('login.html')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        new_user = User(username=user, password=pwd)
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

        found = User.query.filter_by(username=user, password=pwd).first()

        if found:
            return f"Welcome {user} 🎉"
        else:
            return "Wrong username or password ❌"

    return render_template('login.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
