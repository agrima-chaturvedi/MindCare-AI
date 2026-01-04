from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from datetime import datetime
from random import choice
from dateutil.parser import parse  
import os

# -----------------------------
# Flask & Bcrypt Setup
# -----------------------------
app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

# -----------------------------
# Google Gemini Client
# -----------------------------
from google.genai import Client

# Use your API key here
client = Client(api_key="AIzaSyDaDOZLU6lxJbrphrooh9-Ha4K9AAGC4Y4")

def get_gemini_response(prompt):
    """
    Sends prompt to Gemini API and returns the generated text
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # Specify the model name
        contents=[{"text": prompt}]  # Pass the prompt as a list of dictionaries
    )
    return response.text

# -----------------------------
# MongoDB Atlas Connection
# -----------------------------
mongo_client = MongoClient(
    "mongodb+srv://agrimachaturvedi6_db_user:Hellomahi1@cluster0.f2qcdcn.mongodb.net/mental_wellness_db?retryWrites=true&w=majority"
)
db = mongo_client["mental_wellness_db"]
users = db["users"]
moods_collection = db["moods"]
journal_collection = db["journal"]
chat_collection = db["chat"]

# -----------------------------
# Mood Suggestions Dataset
# -----------------------------
mood_suggestions_dataset = {
    "happy": [
        "Keep smiling! 😊 Listen to your favorite song.",
        "Share your happiness with a friend.",
        "Celebrate your small wins today!"
    ],
    "sad": [
        "Try a 5-minute deep breathing exercise.",
        "Write down one thing you're grateful for today.",
        "Go for a short walk or stretch."
    ],
    "angry": [
        "Take a short walk or stretch to release tension.",
        "Practice deep breathing to calm down.",
        "Write down what’s making you angry and why."
    ],
    "anxious": [
        "Try a quick mindfulness meditation.",
        "Do 5 minutes of deep breathing exercises.",
        "Write down your thoughts to clear your mind."
    ],
    "neutral": [
        "Reflect on your day in your journal.",
        "Take a short break to stretch and relax.",
        "Drink a glass of water and breathe deeply."
    ],
    "unknown": [
        "Take a moment to relax and breathe deeply.",
        "Check in with your feelings and write them down.",
        "Do something small that brings you joy."
    ]
}
import random

def get_random_background(gender):
    folder = f"static/images/{gender}"
    images = os.listdir(folder)
    return f"{folder}/{random.choice(images)}"

# -----------------------------
# Routes
# -----------------------------
app.config['UPLOAD_FOLDER'] = "static/uploads"

# Create folder if missing
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    # 🔒 PROTECT THIS PAGE
    if "user_id" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))

    user_id = session["user_id"]  # safe now

    if request.method == 'POST':
        image = request.files['photo']

        filename = f"{user_id}.jpg"   # ✔ no more KeyError
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save the filename so it can be used in dashboard
        session['photo'] = filename

        return redirect('/dashboard')
    images = ["1.jpeg", "2.jpeg", "3.jpeg","download(1).jpeg","download(2).jpeg","download(3).jpeg",
              "download(4).jpeg","download(5).jpeg","download.jpeg","23.jpeg","45.jpeg","78.jpeg",
              "9.jpeg","10.jpeg","11.jpeg","12.jpeg","13.jpeg","15.jpeg","Value.jpeg"]
    selected_bg = random.choice(images)

    return render_template('upload_photo.html',bg_image=selected_bg)


@app.route("/")
def index():
    images = ["1.jpeg", "2.jpeg", "3.jpeg","download(1).jpeg","download(2).jpeg","download(3).jpeg",
              "download(4).jpeg","download(5).jpeg","download.jpeg","23.jpeg","45.jpeg","78.jpeg",
              "9.jpeg","10.jpeg","11.jpeg","12.jpeg","13.jpeg","15.jpeg","Value.jpeg"]
    selected_bg = random.choice(images)
    return render_template("index.html", bg_image=selected_bg)



# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please fill out both fields.", "warning")
            return redirect(url_for("signup"))

        if users.find_one({"username": username}):
            flash("User already exists!", "danger")
            return redirect(url_for("signup"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        users.insert_one({"username": username, "password": hashed_password})
        flash("Signup successful! Please login.", "success")
        return redirect(url_for("login"))
    images= ["1.jpeg", "2.jpeg", "3.jpeg","download(1).jpeg","download(2).jpeg","download(3).jpeg",
              "download(4).jpeg","download(5).jpeg","download.jpeg","23.jpeg","45.jpeg","78.jpeg",
              "9.jpeg","10.jpeg","11.jpeg","12.jpeg","13.jpeg","15.jpeg","Value.jpeg"]
    selected_bg = random.choice(images)
    return render_template("signup.html",bg_image=selected_bg)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = users.find_one({"username": username})

        if user and bcrypt.check_password_hash(user["password"], password):

            # 🔥 ADD THESE TWO LINES
            session["username"] = username
            session["user_id"] = str(user["_id"])   # Store user ID safely

            flash(f"Welcome, {username}!", "success")
            return redirect(url_for("upload_photo"))

        flash("Invalid credentials!", "danger")
        return redirect(url_for("login"))
    images = ["1.jpeg", "2.jpeg", "3.jpeg","download(1).jpeg","download(2).jpeg","download(3).jpeg",
              "download(4).jpeg","download(5).jpeg","download.jpeg","23.jpeg","45.jpeg","78.jpeg",
              "9.jpeg","10.jpeg","11.jpeg","12.jpeg","13.jpeg","15.jpeg","Value.jpeg"]
    selected_bg = random.choice(images)
    return render_template("login.html",bg_image=selected_bg)

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session["username"])
    flash("Please login first.", "warning")
    return redirect(url_for("login"))

# Mood Tracker
@app.route('/mood', methods=['GET', 'POST'])
def mood():
    if request.method == 'POST':
        mood_value = request.form.get('mood')
        note = request.form.get('note', '')

        # Gemini analysis
        gemini_prompt = f"Analyze the mood from this note: {note}"
        gemini_analysis = get_gemini_response(gemini_prompt)

        moods_collection.insert_one({
            "mood": mood_value,
            "note": note,
            "gemini_analysis": gemini_analysis,
            "date": datetime.now()
        })

        suggestion = choice(mood_suggestions_dataset.get(mood_value, mood_suggestions_dataset["unknown"]))
        recent_moods = list(moods_collection.find().sort('date', -1).limit(5))

        return render_template("mood.html", recent_moods=recent_moods, suggestion=suggestion)
    images = ["1.jpeg", "2.jpeg", "3.jpeg","download(1).jpeg","download(2).jpeg","download(3).jpeg",
              "download(4).jpeg","download(5).jpeg","download.jpeg","23.jpeg","45.jpeg","78.jpeg",
              "9.jpeg","10.jpeg","11.jpeg","12.jpeg","13.jpeg","15.jpeg","Value.jpeg"]
    selected_bg = random.choice(images)
    recent_moods = list(moods_collection.find().sort('date', -1).limit(5))
    return render_template("mood.html", recent_moods=recent_moods,bg_image=selected_bg)

# Journal
@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        title = request.form.get('title', 'Untitled')
        content = request.form.get('content', '')

        gemini_prompt = f"Analyze the sentiment of this journal entry: {content}"
        sentiment_analysis = get_gemini_response(gemini_prompt)

        journal_collection.insert_one({
            "title": title,
            "content": content,
            "sentiment_analysis": sentiment_analysis,
            "date": datetime.now()
        })

        suggestion = choice(mood_suggestions_dataset.get(sentiment_analysis, mood_suggestions_dataset["unknown"]))
        recent_entries = list(journal_collection.find().sort('date', -1).limit(10))

        return render_template("journal.html", recent_entries=recent_entries, suggestion=suggestion)

    recent_entries = list(journal_collection.find().sort('date', -1).limit(10))
    images = ["1.jpeg", "2.jpeg", "3.jpeg","download(1).jpeg","download(2).jpeg","download(3).jpeg",
              "download(4).jpeg","download(5).jpeg","download.jpeg","23.jpeg","45.jpeg","78.jpeg",
              "9.jpeg","10.jpeg","11.jpeg","12.jpeg","13.jpeg","15.jpeg","Value.jpeg"]
    selected_bg = random.choice(images)
    return render_template("journal.html", recent_entries=recent_entries,bg_image=selected_bg)

# Analytics


@app.route('/analytics')
def analytics():
    moods = list(moods_collection.find())
    journal_moods = list(journal_collection.find())

    all_moods = [entry.get('mood', 'okk') for entry in moods] + \
                [entry.get('mood', 'fine') for entry in journal_moods]

    from collections import Counter
    mood_counts = dict(Counter(all_moods))

    combined_entries = moods + journal_moods

    # Convert string dates to datetime before sorting
    for entry in combined_entries:
        if isinstance(entry.get('date'), str):
            entry['date'] = parse(entry['date'])

    # Sort safely by datetime
    combined_entries.sort(key=lambda x: x['date'])

    trend_labels = [entry['date'].strftime("%Y-%m-%d") for entry in combined_entries]
    trend_data = [entry.get('mood', 'unknown') for entry in combined_entries]

    gemini_prompt = f"Provide insights on the following mood data: {mood_counts}"
    gemini_insights = get_gemini_response(gemini_prompt)
    images = ["1.jpeg", "2.jpeg", "3.jpeg","download(1).jpeg","download(2).jpeg","download(3).jpeg",
              "download(4).jpeg","download(5).jpeg","download.jpeg","23.jpeg","45.jpeg","78.jpeg",
              "9.jpeg","10.jpeg","11.jpeg","12.jpeg","13.jpeg","15.jpeg","Value.jpeg"]
    selected_bg = random.choice(images)
    return render_template(
        'analytics.html',
        chart_data=mood_counts,
        trend_labels=trend_labels,
        trend_data=trend_data,
        gemini_insights=gemini_insights,
        bg_image=selected_bg
    )

# Chatbot
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if "username" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    bot_response = None
    user_message = None

    if request.method == "POST":
        user_message = request.form.get("message", "").strip()
        if user_message:
            bot_response = get_gemini_response(user_message)

            # Store in DB
            chat_collection.insert_one({
                "username": session["username"],
                "user_message": user_message,
                "bot_response": bot_response,
                "date": datetime.now()
            })
    images = ["1.jpeg", "2.jpeg", "3.jpeg","download(1).jpeg","download(2).jpeg","download(3).jpeg",
              "download(4).jpeg","download(5).jpeg","download.jpeg","23.jpeg","45.jpeg","78.jpeg",
              "9.jpeg","10.jpeg","11.jpeg","12.jpeg","13.jpeg","15.jpeg","Value.jpeg"]
    selected_bg = random.choice(images)
    return render_template("chatbot.html", user_message=user_message, bot_response=bot_response,bg_image=selected_bg)

# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    session.pop("photo", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

# -----------------------------
# Run the App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
