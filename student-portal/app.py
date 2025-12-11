from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="student_portal"
)

# ------------------------ ROUTES -----------------------------

@app.route("/")
def home():
    return redirect("/login")

# ------------------- REGISTER PAGE -------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        cur = db.cursor()
        cur.execute("SELECT * FROM students WHERE email=%s", (email,))
        account = cur.fetchone()

        if account:
            msg = "⚠ Email already exists. Try login."
        else:
            cur.execute("INSERT INTO students (name, email, password) VALUES (%s, %s, %s)",
                        (name, email, hashed_password))
            db.commit()
            msg = "🎉 Registered Successfully! Please Login."

    return render_template("register.html", message=msg)

# --------------------- LOGIN PAGE --------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM students WHERE email=%s", (email,))
        user = cur.fetchone()

        if user and check_password_hash(user["password"], password):
            session["logged_in"] = True
            session["name"] = user["name"]
            session["email"] = user["email"]
            return redirect("/dashboard")
        else:
            msg = "❌ Incorrect Email or Password"

    return render_template("login.html", message=msg)

# ---------------------- DASHBOARD --------------------------

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")

    return render_template("dashboard.html", name=session["name"])

# ---------------------- LOGOUT -----------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0")

