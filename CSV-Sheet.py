import pandas as pd
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRET_FILE = '-'

def authenticate_google():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    client = gspread.authorize(creds)
    return client

client = authenticate_google()

sheet_title = "Spotify_History"
sh = client.open(sheet_title)
worksheet = sh.sheet1

sh.share('alicewarren54@gmail.com', perm_type='user', role='writer')

worksheet = sh.get_worksheet(0)

csv_path = '2014_06July2025cleaned.csv'
df = pd.read_csv(csv_path)

values = [df.columns.values.tolist()] + df.values.tolist()a
worksheet.update('A1', values)

print("CSV data uploaded to Google Sheet successfully")