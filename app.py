from flask import Flask, render_template, request, redirect, session, url_for
from supabase import create_client, Client
from dotenv import load_dotenv

import os
load_dotenv()  # Loads variables from .env
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")





#app.secret_key = os.environ.get("FLASK_SECRET_KEY")  # Now pulls from .env

# Supabase setup
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def home():
    # Check if user is logged in
    if "user" in session:
        return f"Welcome, {session['user']['email']}! <a href='/logout'>Logout</a>"
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        # Supabase login
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            session["user"] = user.model_dump()  # Store user in session
            return redirect("/")
        except Exception as e:
            return f"Login failed: {e}"
    
    return render_template("index.html", action="login")

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    password = request.form["password"]
    
    # Supabase signup
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        session["user"] = user.model_dump()
        return redirect("/")
    except Exception as e:
        return f"Signup failed: {e}"

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
