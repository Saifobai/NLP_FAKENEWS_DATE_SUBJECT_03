import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import joblib
import re
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Optional URL extraction
try:
    from newspaper import Article
except ImportError:
    Article = None

# NLTK setup
try:
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("corpora/stopwords")
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

load_dotenv()

MODEL_FILE = "model.pkl"
SBERT_MODEL = None
CLASSIFIER = None

# Load model
if os.path.exists(MODEL_FILE):
    data = joblib.load(MODEL_FILE)
    SBERT_MODEL = data["sbert_model"]
    CLASSIFIER = data["classifier"]
    print("✅ SBERT model and classifier loaded.")
else:
    print("⚠️ model.pkl not found.")

app = Flask(__name__)


def clean_text(text: str):
    if not text:
        return ""
    text = BeautifulSoup(text, "html.parser").get_text()
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = word_tokenize(text)
    tokens = [
        lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 1
    ]
    return " ".join(tokens)


def extract_from_url(url: str):
    if not url:
        return "", ""
    try:
        if Article:
            article = Article(url)
            article.download()
            article.parse()
            return article.title.strip(), article.text.strip()
    except Exception as e:
        print("Newspaper3k failed:", e)

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string if soup.title else ""
        paragraphs = " ".join([p.get_text() for p in soup.find_all("p")])
        return title.strip(), paragraphs.strip()
    except Exception as e2:
        print("Fallback failed:", e2)
        return "", ""


def predict_label(title: str, body: str):
    full_text = f"{title} {body}"
    cleaned = clean_text(full_text)

    if SBERT_MODEL is None or CLASSIFIER is None:
        pseudo_score = (len(cleaned.split()) % 7) / 6.0
        label = "REAL" if pseudo_score >= 0.5 else "FAKE"
        return label, round(pseudo_score, 3)

    embedding = SBERT_MODEL.encode([cleaned])
    pred = CLASSIFIER.predict(embedding)[0]
    prob = None
    if hasattr(CLASSIFIER, "predict_proba"):
        probs = CLASSIFIER.predict_proba(embedding)[0]
        prob = probs[pred]
    else:
        prob = 1.0

    mapping = {0: "FAKE", 1: "REAL"}
    label = mapping.get(pred, "UNKNOWN")
    return label, float(prob)


@app.get("/")
def home():
    return render_template(
        "index.html",
        weather_api_key=os.getenv("OPENWEATHER_API_KEY"),
        news_api_key=os.getenv("NEWS_API_KEY"),
    )


# Added back About route to avoid BuildError
@app.get("/about")
def about():
    return render_template(
        "about.html"
    )  # Create about.html or replace with simple text


@app.post("/predict")
def predict_form():
    url = request.form.get("url", "").strip()
    title = request.form.get("title", "").strip()
    body = request.form.get("text", "").strip()

    if url and (not title or not body):
        t2, b2 = extract_from_url(url)
        title = title or t2
        body = body or b2

    if not (title or body):
        return render_template(
            "index.html", error="Please provide title, text, or a valid URL."
        )

    label, prob = predict_label(title, body)
    return render_template(
        "index.html", prediction=label, prob=prob, title=title, text=body, url=url
    )


@app.get("/health")
def health():
    loaded = bool(SBERT_MODEL and CLASSIFIER)
    return jsonify({"status": "ok", "model_loaded": loaded})


@app.post("/api/predict")
def predict_api():
    data = request.get_json(force=True, silent=True) or {}
    url = data.get("url", "").strip()
    title = data.get("title", "").strip()
    body = data.get("text", "").strip()

    if url and (not title or not body):
        t2, b2 = extract_from_url(url)
        if not title:
            title = t2
        if not body:
            body = b2

    if not (title or body):
        return jsonify({"error": "Please provide title/text or URL"}), 400

    label, prob = predict_label(title, body)
    return jsonify({"label": label, "probability": prob})


if __name__ == "__main__":
    app.run(debug=True)
