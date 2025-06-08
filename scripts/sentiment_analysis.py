import pandas as pd
from transformers import pipeline
import os
from tqdm import tqdm

tqdm.pandas()  # Progress bar

CLEAN_PATH = os.path.join("/content", "drive", "MyDrive", "10Acadamy","bank_reviews_clean.csv")
OUTPUT_PATH = os.path.join("/content", "drive", "MyDrive", "10Acadamy", "bank_reviews_with_sentiment.csv")

# Load Hugging Face sentiment model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def classify_sentiment_with_neutral(text, neutral_threshold=0.65):
    try:
        result = sentiment_pipeline(text[:512])[0]  # Truncate long reviews
        score = result["score"]
        label = result["label"].lower()

        # Convert to neutral if score is weak
        if score < neutral_threshold:
            return pd.Series(["neutral", score])
        return pd.Series([label, score])

    except Exception:
        return pd.Series(["unknown", 0.0])

def apply_sentiment():
    df = pd.read_csv(CLEAN_PATH)
    print(f"🔍 Loaded {len(df)} cleaned reviews")

    df[["sentiment_label", "sentiment_score"]] = df["review"].progress_apply(classify_sentiment_with_neutral)

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Sentiment scores with neutral labels saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    apply_sentiment()
