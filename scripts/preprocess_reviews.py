import pandas as pd
import os


RAW_PATH = os.path.join("/content","drive","MyDrive","10Acadamy","bank_reviews_raw.csv")
CLEAN_PATH = os.path.join("/content","drive","MyDrive","10Acadamy", "bank_reviews_clean.csv")

def clean_reviews(raw_csv=RAW_PATH, output_csv=CLEAN_PATH):
  print(f"📥 Loading data from: {raw_csv}")
  df = pd.read_csv(raw_csv)

  print(f"🔍 Original shape: {df.shape}")

  df = df.dropna(subset=["review", "rating", "date", "bank"])

  df = df.drop_duplicates(subset=["review", "bank"])

  df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

  df = df.dropna(subset=["date"])

  print(f"✅ Cleaned shape: {df.shape}")

  df.to_csv(output_csv, index=False)
  print(f"📦 Cleaned data saved to: {output_csv}")

if __name__ == "__main__":
  clean_reviews()