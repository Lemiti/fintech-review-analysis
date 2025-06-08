import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Paths
INPUT_PATH = os.path.join("/content", "drive", "MyDrive", "10Acadamy","bank_reviews_with_sentiment.csv")
OUTPUT_PATH = os.path.join("/content", "drive", "MyDrive", "10Acadamy", "top_keywords_per_bank.csv")

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return " ".join(tokens)

def extract_keywords(df, top_n=10):
    results = []

    for bank in df["bank"].unique():
        print(f"🔍 Processing keywords for: {bank}")
        bank_reviews = df[df["bank"] == bank]["review"].dropna().astype(str)
        bank_reviews = bank_reviews.apply(preprocess_text)

        vectorizer = TfidfVectorizer(max_df=0.85, max_features=1000)
        tfidf_matrix = vectorizer.fit_transform(bank_reviews)
        tfidf_scores = tfidf_matrix.sum(axis=0).A1
        feature_names = vectorizer.get_feature_names_out()

        keywords = sorted(zip(feature_names, tfidf_scores), key=lambda x: -x[1])[:top_n]

        for word, score in keywords:
            results.append({"bank": bank, "keyword": word, "score": round(score, 3)})

    return pd.DataFrame(results)

def run_keyword_extraction():
    df = pd.read_csv(INPUT_PATH)
    df_keywords = extract_keywords(df, top_n=15)
    df_keywords.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Keywords saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    run_keyword_extraction()
