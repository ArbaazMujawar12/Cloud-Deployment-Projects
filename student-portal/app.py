from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # change to a secure random value in production
app.permanent_session_lifetime = timedelta(hours=6)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "student_portal",
    "auth_plugin": "mysql_native_password"
}

def get_db_connection():
    """Return a new DB connection. Use per-request to avoid stale connections."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("DB connection error:", e)
        return None

def is_valid_email(email):
    # Simple regex for email validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# ------------------------ ROUTES -----------------------------

@app.route("/")
def home():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

# ------------------- REGISTER PAGE --------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip() or None
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip() or None
        gender = request.form.get("gender", "") or None
        course = request.form.get("course", "").strip() or None
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Basic server-side validation
        if not name or not email or not password or not confirm_password:
            flash("Please fill in all required fields.", "warning")
            return render_template("register.html", form=request.form)

        if not is_valid_email(email):
            flash("Please enter a valid email address.", "warning")
            return render_template("register.html", form=request.form)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "warning")
            return render_template("register.html", form=request.form)

        if password != confirm_password:
            flash("Passwords do not match.", "warning")
            return render_template("register.html", form=request.form)

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        if not conn:
            flash("Database connection error. Try again later.", "danger")
            return render_template("register.html", form=request.form)

        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id FROM students WHERE email=%s", (email,))
            account = cur.fetchone()
            if account:
                flash("Email already registered. Try logging in.", "info")
                return render_template("register.html", form=request.form)

            insert_sql = """
                INSERT INTO students (name, username, email, phone, gender, course, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_sql, (name, username, email, phone, gender, course, hashed_password))
            conn.commit()

            flash("🎉 Registered successfully! Please login.", "success")
            return redirect(url_for("login"))

        except Error as e:
            print("DB error during register:", e)
            flash("An error occurred during registration. Try again.", "danger")
            return render_template("register.html", form=request.form)
        finally:
            cur.close()
            conn.close()

    return render_template("register.html")

# --------------------- LOGIN PAGE ---------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password.", "warning")
            return render_template("login.html")

        conn = get_db_connection()
        if not conn:
            flash("Database connection error. Try again later.", "danger")
            return render_template("login.html")

        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM students WHERE email=%s", (email,))
            user = cur.fetchone()

            if user and check_password_hash(user["password"], password):
                session.permanent = True
                session["logged_in"] = True
                session["user_id"] = user["id"]
                session["name"] = user["name"]
                session["email"] = user["email"]
                flash(f"Welcome back, {user['name']}!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("❌ Incorrect email or password.", "danger")
                return render_template("login.html")
        except Error as e:
            print("DB error during login:", e)
            flash("An error occurred. Try again.", "danger")
            return render_template("login.html")
        finally:
            cur.close()
            conn.close()

    return render_template("login.html")

# ---------------------- DASHBOARD ---------------------------

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        flash("Please login to access the dashboard.", "info")
        return redirect(url_for("login"))

    user = None
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, name, username, email, phone, gender, course, created_at FROM students WHERE id=%s",
                        (session.get("user_id"),))
            user = cur.fetchone()
        except Error as e:
            print("DB error fetch dashboard:", e)
        finally:
            cur.close()
            conn.close()

    return render_template("dashboard.html", user=user)

# ---------------------- LOGOUT ------------------------------

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# ---------------------- PROFILE (Optional) -------------------
# You can add profile edit routes later

# -------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
