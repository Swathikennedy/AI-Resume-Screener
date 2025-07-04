from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import re

# Download stopwords if not already present
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text)  # keep only alphabets
    tokens = text.lower().split()
    filtered = [word for word in tokens if word not in stop_words and len(word) > 2]
    return " ".join(filtered)

def compute_similarity(resume_text, jd_text):
    resume = clean_text(resume_text)
    jd = clean_text(jd_text)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, jd])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return score * 100

def get_missing_keywords(resume_text, jd_text):
    jd_keywords = set(clean_text(jd_text).split())
    resume_keywords = set(clean_text(resume_text).split())
    missing = jd_keywords - resume_keywords
    return sorted(list(missing))
