from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "App is running 🚀"

@app.route('/login')
def login():
    return "Login page"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(200))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        # hash password
        hashed = generate_password_hash(pwd)

        new_user = User(username=user, password=hashed)
        db.session.add(new_user)
        db.session.commit()

        return "Registered Succesfull! Go to /login"

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        found = User.query.filter_by(username=user).first()

        print("User found:", found)
        if found:
            print("Stored password:", found.password)

        if found and check_password_hash(found.password, pwd):
            return f"Welcome {user}"
        else:
            return "Wrong username or password"

    return render_template('login.html')

with app.app_context():
        db.create_all()
    app.run(debug=True)
