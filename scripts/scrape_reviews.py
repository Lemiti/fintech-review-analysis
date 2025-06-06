from google_play_scraper import app, Sort, reviews
import pandas as pd 
from datetime import datetime

def get_reviews(app_id, bank_name, count=400):
  all_reviews = []
  token = None

  while len(all_reviews) < count:
    new_reviews, token = reviews(
      app_id,
      lang='en',
      country='et',
      sort=Sort.NEWEST,
      count=100,
      continuation_token=token
    )
    all_reviews.extend(new_reviews)
    if not token:
      break

  df = pd.DataFrame([{
    'review':r['content'],
    'rating': r['score'],
    'date': r['at'].strftime('%Y-%m-%d'),
    'bank': bank_name,
    'source': 'Google Play'
  } for r in all_reviews[:count]])

  return df

if __name__ == "__main__":
  banks = {
    'com.combanketh.mobilebanking': 'CBE',
    'com.boa.boaMobileBanking': 'BOA',
    'com.dashen.dashensuperapp': 'Dashen'
  }

  all_data = pd.concat(
    [get_reviews(app_id, bank_name) for app_id, bank_name in banks.items()],
    ignore_index=True
  )
  all_data.to_csv('/content/drive/MyDrive/10Acadamy/bank_reviews_raw.csv', index=False)
  print("✅ Reviews scraped and saved to 'bank_reviews_raw.csv'")