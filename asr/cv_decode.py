
#!/usr/bin/env python3

import os
import requests
import pandas as pd
from tqdm import tqdm

def main():
    # 1. Load the CSV file
    csv_file = "cv-valid-dev.csv"
    if not os.path.isfile(csv_file):
        print(f"Error: '{csv_file}' not found in the current folder.")
        return
    
    df = pd.read_csv(csv_file)

    # 2. Prepare to store transcriptions
    transcriptions = []

    # 3. Iterate over rows with a progress bar
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Transcribing files"):
        file_path = row["filename"]  # e.g. "cv-valid-dev/sample-000000.mp3"
        
        # Check if the file exists
        if not os.path.isfile(file_path):
            print(f"Warning: File '{file_path}' not found. Skipping.")
            transcriptions.append("")
            continue
        
        # Send POST request to the ASR endpoint with a 30s timeout
        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f, "audio/mpeg")}
                response = requests.post(
                    "http://localhost:8001/asr", 
                    files=files, 
                    timeout=(15, 30)  # Skip if processing takes more than 30s
                )
                
            if response.status_code == 200:
                data = response.json()
                transcription = data.get("transcription", "")
            else:
                print(f"\nError: Received status code {response.status_code} for file '{file_path}'")
                transcription = ""

        except requests.exceptions.Timeout:
            print(f"\nWarning: File '{file_path}' took longer than 30s. Skipping.")
            transcription = ""
        except Exception as e:
            print(f"\nError: Could not process '{file_path}'. Reason: {str(e)}")
            transcription = ""
        
        transcriptions.append(transcription)
    
    # 4. Insert or update the generated text in a new column
    df["generated_text"] = transcriptions

    # 5. Overwrite the same CSV file with the new column
    df.to_csv(csv_file, index=False)
    print(f"\nUpdated CSV file '{csv_file}' with new column 'generated_text'.")

if __name__ == "__main__":
    main()
