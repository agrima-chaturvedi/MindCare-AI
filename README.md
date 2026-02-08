# 🧠 AI-Based Mental Wellness Assistant

An AI-powered Mental Wellness Assistant designed to support users in tracking emotions, journaling thoughts, and receiving personalized wellness suggestions. The system combines NLP, sentiment analysis, and a conversational chatbot to promote emotional awareness and mental well-being.

---

## ✨ Features

* **Conversational Chatbot**
  Friendly AI chatbot for daily check-ins, emotional support, and basic mental wellness guidance.

* **Mood Tracking**
  Users can log daily moods; the system visualizes emotional patterns over time.

* **AI Journal**
  Secure journaling space where users can write freely. NLP models analyze sentiment and emotional tone.

* **Sentiment Analysis**
  Uses NLP techniques to detect emotions such as happiness, sadness, stress, anxiety, or neutrality.

* **Wellness Recommendations**
  Suggests activities like breathing exercises, meditation, journaling prompts, music, or short breaks based on mood trends.

* **User Authentication**
  Secure login and signup system to protect personal mental health data.

* **Dashboard & Insights**
  Visual charts and summaries showing mood trends and emotional progress.

---

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js (for mood visualization)

### Backend

* Python
* Flask (Web Framework)

### AI / NLP

* spaCy / NLTK / BERT (Sentiment Analysis)
* Machine Learning models for emotion detection

### Database

* MongoDB (for user data, journal entries, mood logs)

---

## 🏗️ System Architecture

1. User interacts with the web interface
2. Requests are sent to Flask backend
3. NLP model analyzes text input
4. Sentiment results are stored in database
5. Recommendation engine suggests wellness activities
6. Dashboard displays insights and trends

---

## 📂 Project Structure

```
mental-wellness-assistant/
│
├── app.py                 # Main Flask application
├── models/                # ML & NLP models
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── database/              # MongoDB connection & schemas
├── utils/                 # Helper functions
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 🚀 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/mental-wellness-assistant.git
   cd mental-wellness-assistant
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   flask run
   ```

5. Open browser and go to:

   ```
   http://127.0.0.1:5000/
   ```

---

## 🔐 Privacy & Ethics

* User data is securely stored and never shared
* The assistant does **not** replace professional mental health care
* Provides support and awareness, not medical diagnosis

---

## 📈 Future Enhancements

* Voice-based interaction
* Multilingual support
* Integration with wearable devices
* Advanced emotion detection (stress level, burnout)
* Therapist / counselor recommendation

---

## 👩‍💻 Author

**Agrima Chaturvedi**
AI & Web Development Enthusiast

---

## 📜 Disclaimer

This project is for educational and wellness-support purposes only. For serious mental health concerns, please consult a certified mental health professional.
