import pandas as pd
import os


# Input and output paths
INPUT_PATH = os.path.join("/content", "drive", "MyDrive", "10Acadamy", "top_keywords_per_bank.csv")
OUTPUT_PATH = os.path.join("/content", "drive", "MyDrive", "10Acadamy", "bank_themes.csv")


def assign_themes_manually():
   df = pd.read_csv(INPUT_PATH)


   print("🔍 Top keywords loaded. Now assigning themes...")


   # Create an empty list to store results
   records = []


   for _, row in df.iterrows():
       bank = row["bank"]
       keyword = row["keyword"]


       print(f"\nBank: {bank}\nKeyword: '{keyword}'")
       theme = input("👉 Enter a theme for this keyword (e.g., Login Issues, UI/UX, Transactions, Support): ")


     
       records.append({
           "bank": bank,
           "theme": theme,
           "keyword": keyword,
       })


   # Convert to DataFrame
   result_df = pd.DataFrame(records)


   # Group keywords by theme
   grouped_df = result_df.groupby(["bank", "theme"]).agg({
       "keyword": lambda x: ", ".join(sorted(set(x)))
      
   }).reset_index()


   # Save to CSV
   grouped_df.to_csv(OUTPUT_PATH, index=False)
   print(f"\n✅ Theme mapping saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
   assign_themes_manually()
