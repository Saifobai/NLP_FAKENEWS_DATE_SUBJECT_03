# preprocessing.py
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download NLTK resources only the first time; harmless if repeated.
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

_stop_words = set(stopwords.words("english"))
_lemmatizer = WordNetLemmatizer()


def preprocess_text(text: str) -> str:
    """
    Lowercase, remove punctuation/numbers, tokenize, remove stopwords, lemmatize.
    Kept lightweight so it matches the training pipeline.
    """
    text = (text or "").lower()
    text = re.sub(r"[^a-z\s]", " ", text)  # keep only letters & spaces
    tokens = word_tokenize(text)
    tokens = [_lemmatizer.lemmatize(w) for w in tokens if w and w not in _stop_words]
    return " ".join(tokens)
