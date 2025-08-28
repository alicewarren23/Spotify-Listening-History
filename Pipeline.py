import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe
import os

def to_iso_format(val):
    if pd.isna(val):
        return None
    try:
        clean_val = str(val).replace(" at ", " ")
        dt = pd.to_datetime(clean_val, errors="coerce")
        if pd.isna(dt):
            return None
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("lucid-parsec-464412-t8-75d0c2e2a5fa.json", scope)
client = gspread.authorize(creds)


sheet = client.open('Recent Spotify Plays').sheet1
new_df = get_as_dataframe(sheet, evaluate_formulas=True).dropna(how="all")
new_df["Date/Time"] = new_df["Date/Time"].apply(to_iso_format)


new_df = new_df.drop(columns=['URI'], errors='ignore')


output_file = 'Spotify-History-ISO-Current.csv'
if os.path.exists(output_file):
    existing_df = pd.read_csv(output_file)
    
    combined_df = pd.concat([existing_df, new_df]).drop_duplicates()
    
    combined_df = combined_df.sort_values('Date/Time', ascending=False)
else:
    combined_df = new_df


combined_df.to_csv(output_file, index=False)

print(f"Data processed and saved to {output_file}")
print(f"Total records: {len(combined_df)}")