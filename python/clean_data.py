# clean_data.py

import pandas as pd
import os

def clean_data(input_file, output_file):
    print("🔄 Cleaning data...")

    df = pd.read_csv(input_file)

    # ✅ Rename PublishedAt → UploadDate for consistency
    df = df.rename(columns={"PublishedAt": "UploadDate"})

    # Convert UploadDate to datetime
    df["UploadDate"] = pd.to_datetime(df["UploadDate"], errors="coerce")

    # Ensure numeric columns
    df["Views"] = pd.to_numeric(df["Views"], errors="coerce").fillna(0).astype(int)
    df["Likes"] = pd.to_numeric(df["Likes"], errors="coerce").fillna(0).astype(int)
    df["Comments"] = pd.to_numeric(df["Comments"], errors="coerce").fillna(0).astype(int)

    # Drop duplicates
    df = df.drop_duplicates(subset=["VideoID"])

    # Drop rows with missing critical data
    df = df.dropna(subset=["UploadDate", "Title"])

    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"✅ Cleaned data saved to {output_file}")


if __name__ == "__main__":
    # Paths
    raw_file = os.path.join("..", "data", "raw", "YouTubeData.csv")
    processed_file = os.path.join("..", "data", "processed", "YouTubeData_Cleaned.csv")

    # Create processed directory if not exists
    os.makedirs(os.path.dirname(processed_file), exist_ok=True)

    # Run cleaning
    clean_data(raw_file, processed_file)
