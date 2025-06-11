import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# Download NLTK resources with error handling
try:
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('punkt_tab')  # Critical addition
except Exception as e:
   print(f"Error downloading NLTK resources: {e}")


# Paths (verify these exist!)
INPUT_PATH = os.path.join("/content", "drive", "MyDrive", "10Acadamy", "bank_reviews_with_sentiment.csv")
OUTPUT_PATH = os.path.join("/content", "drive", "MyDrive", "10Acadamy", "top_keywords_per_bank.csv")


def preprocess_text(text):
   """Handle non-string inputs and tokenization errors."""
   if not isinstance(text, str):
       return ""
   try:
       tokens = word_tokenize(text.lower())
       stop_words = set(stopwords.words("english"))
       tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
       return " ".join(tokens)
   except Exception as e:
       print(f"Error processing text: {e}")
       return ""


def extract_keywords(df, top_n=10):
   """Extract keywords with TF-IDF, skipping empty reviews."""
   results = []
  
   for bank in df["bank"].unique():
       print(f"🔍 Processing keywords for: {bank}")
       bank_reviews = df[df["bank"] == bank]["review"].dropna().astype(str)
      
       # Skip if no valid reviews
       if bank_reviews.empty:
           print(f"⚠️ No valid reviews for {bank}")
           continue
          
       # Preprocess in batches if memory is an issue
       try:
           bank_reviews = bank_reviews.apply(preprocess_text)
           vectorizer = TfidfVectorizer(max_df=0.85, max_features=1000)
           tfidf_matrix = vectorizer.fit_transform(bank_reviews)
           tfidf_scores = tfidf_matrix.sum(axis=0).A1
           feature_names = vectorizer.get_feature_names_out()
          
           keywords = sorted(zip(feature_names, tfidf_scores), key=lambda x: -x[1])[:top_n]
           for word, score in keywords:
               results.append({"bank": bank, "keyword": word, "score": round(score, 3)})
              
       except Exception as e:
           print(f"❌ Failed to process {bank}: {e}")
          
   return pd.DataFrame(results)


def run_keyword_extraction():
   """Main function with file validation."""
   if not os.path.exists(INPUT_PATH):
       raise FileNotFoundError(f"Input file not found at {INPUT_PATH}")
      
   df = pd.read_csv(INPUT_PATH)
   print(f"✅ Loaded {len(df)} reviews")
  
   df_keywords = extract_keywords(df, top_n=15)
  
   os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
   df_keywords.to_csv(OUTPUT_PATH, index=False)
   print(f"✅ Keywords saved to: {OUTPUT_PATH}")
   print(df_keywords.head())


if __name__ == "__main__":
   run_keyword_extraction()
