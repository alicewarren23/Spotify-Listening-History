import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Spotify Listening History Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1DB954;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #1DB954;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1DB954;
    }
    .stButton > button {
        background-color: #1DB954;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #1ed760;
    }
    .sidebar .stSelectbox > label {
        color: #1DB954;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def load_credentials():
    """Load Google Sheets credentials"""
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Try to load from Streamlit secrets (for cloud deployment)
        if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
            creds = ServiceAccountCredentials.from_json_keyfile_dict(
                dict(st.secrets['google_sheets']), scope
            )
        else:
            # Fallback to local JSON file (for local development)
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                "lucid-parsec-464412-t8-75d0c2e2a5fa.json", scope
            )
        
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error loading credentials: {e}")
        st.info("💡 For cloud deployment, make sure to add your Google Sheets credentials to Streamlit secrets.")
        return None

def download_sheet_data(client, sheet_name, output_filename):
    """Download data from Google Sheet"""
    try:
        sheet = client.open(sheet_name).sheet1
        
        with open(output_filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(sheet.row_values(1))  # Write header
            writer.writerows(sheet.get_all_values()[1:])  # Write data
        
        return True
    except Exception as e:
        st.error(f"Error downloading {sheet_name}: {e}")
        return False

def process_data():
    """Complete data processing pipeline"""
    
    # Check if we have existing processed data
    processed_file = "Spotify_History2014-Recent-ISO.csv"
    
    if os.path.exists(processed_file):
        df = pd.read_csv(processed_file)
        df['Date/Time'] = pd.to_datetime(df['Date/Time'])
        return df
    
    # If no processed data, we need to run the transformation
    st.warning("No processed data found. Please run the data update process first.")
    return None

def create_time_analysis(df):
    """Create time-based analysis charts"""
    # Prepare data
    df["Date"] = df["Date/Time"].dt.date
    df["Hour"] = df["Date/Time"].dt.hour
    df["Weekday"] = df["Date/Time"].dt.day_name()
    df["Month"] = df["Date/Time"].dt.month_name()
    
    # Daily trend with rolling average
    daily_counts = df.groupby('Date').size().reset_index(name='count')
    daily_counts['rolling_avg'] = daily_counts['count'].rolling(window=7, center=True).mean()
    
    fig_daily = px.line(daily_counts, x='Date', y='rolling_avg',
                       title="Daily Listening Activity (7-day rolling average)",
                       labels={'rolling_avg': 'Songs per day', 'Date': 'Date'})
    fig_daily.update_traces(line_color='#1DB954', line_width=3)
    fig_daily.update_layout(height=400)
    
    return fig_daily

def create_top_content_charts(df, days_filter=365):
    """Create top songs and artists charts"""
    
    # Filter for recent data if specified
    if days_filter:
        cutoff_date = df['Date/Time'].max() - pd.Timedelta(days=days_filter)
        df_filtered = df[df['Date/Time'] >= cutoff_date].copy()
    else:
        df_filtered = df.copy()
    
    # Top artists
    top_artists = df_filtered["Artist"].value_counts().head(10)
    fig_artists = px.bar(
        x=top_artists.values, 
        y=top_artists.index,
        orientation='h',
        title=f"Top 10 Artists - Last {days_filter} days" if days_filter else "Top 10 Artists - All Time",
        labels={'x': 'Number of Plays', 'y': 'Artist'},
        color=top_artists.values,
        color_continuous_scale='Viridis'
    )
    fig_artists.update_layout(height=500, showlegend=False)
    
    # Top songs
    top_songs = df_filtered.groupby(["Song Name", "Artist"]).size().sort_values(ascending=False).head(10)
    song_labels = [f"{song} - {artist}" for (song, artist) in top_songs.index]
    
    fig_songs = px.bar(
        x=top_songs.values,
        y=[label[:40] + '...' if len(label) > 40 else label for label in song_labels],
        orientation='h',
        title=f"Top 10 Songs - Last {days_filter} days" if days_filter else "Top 10 Songs - All Time",
        labels={'x': 'Number of Plays', 'y': 'Song'},
        color=top_songs.values,
        color_continuous_scale='Plasma'
    )
    fig_songs.update_layout(height=500, showlegend=False)
    
    return fig_artists, fig_songs

def create_pattern_analysis(df, days_filter=365):
    """Create listening pattern analysis"""
    
    # Filter data
    if days_filter:
        cutoff_date = df['Date/Time'].max() - pd.Timedelta(days=days_filter)
        df_filtered = df[df['Date/Time'] >= cutoff_date].copy()
    else:
        df_filtered = df.copy()
    
    df_filtered["Hour"] = df_filtered["Date/Time"].dt.hour
    df_filtered["Weekday"] = df_filtered["Date/Time"].dt.day_name()
    
    # Hourly pattern
    hourly_counts = df_filtered["Hour"].value_counts().sort_index()
    fig_hourly = px.bar(
        x=hourly_counts.index,
        y=hourly_counts.values,
        title="Listening Pattern by Hour of Day",
        labels={'x': 'Hour of Day', 'y': 'Number of Plays'},
        color=hourly_counts.values,
        color_continuous_scale='Sunset'
    )
    fig_hourly.update_layout(height=400, showlegend=False)
    
    # Weekday pattern
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_counts = df_filtered["Weekday"].value_counts().reindex(weekday_order)
    
    fig_weekday = px.bar(
        x=weekday_counts.index,
        y=weekday_counts.values,
        title="Listening Pattern by Day of Week",
        labels={'x': 'Day of Week', 'y': 'Number of Plays'},
        color=weekday_counts.values,
        color_continuous_scale='Rainbow'
    )
    fig_weekday.update_layout(height=400, showlegend=False)
    
    return fig_hourly, fig_weekday

# Main Dashboard
def main():
    # Header
    st.markdown('<h1 class="main-header">🎵 Spotify Listening History Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("⚙️ Dashboard Controls")
    
    # Data Management Section
    st.sidebar.markdown("### 📊 Data Management")
    
    if st.sidebar.button("🔄 Update Data from Google Sheets"):
        with st.spinner("Updating data from Google Sheets..."):
            client = load_credentials()
            if client:
                # Download both sheets
                if download_sheet_data(client, "Spotify History", "Spotify_History.csv"):
                    st.sidebar.success("✅ Historical data updated!")
                
                if download_sheet_data(client, "Recent Spotify Plays", "Recent_Spotify_History.csv"):
                    st.sidebar.success("✅ Recent data updated!")
                    
                    # Process and combine data
                    try:
                        # Load and clean recent data
                        df_recent = pd.read_csv("Recent_Spotify_History.csv")
                        if "URI" in df_recent.columns:
                            df_recent = df_recent.drop(columns=["URI"])
                        df_recent.to_csv("Recent_Spotify_History.csv", index=False)
                        
                        # Combine with historical data
                        history_df = pd.read_csv("Archived_CSV/Spotify_History2014-Aug2025.csv")
                        combined_df = pd.concat([history_df, df_recent], ignore_index=True)
                        combined_df = combined_df.drop_duplicates()
                        combined_df.to_csv("Spotify_History2014-Recent.csv", index=False)
                        
                        # Convert dates to ISO format
                        def convert_to_iso_format(date_str):
                            date_str = str(date_str).strip('"')
                            
                            if 'T' in date_str and date_str.endswith('Z'):
                                return date_str
                            
                            if ' at ' in date_str:
                                try:
                                    dt = datetime.strptime(date_str, "%B %d, %Y at %I:%M%p")
                                    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                                except ValueError:
                                    return date_str
                            return date_str
                        
                        combined_df['Date/Time'] = combined_df['Date/Time'].apply(convert_to_iso_format)
                        combined_df.to_csv('Spotify_History2014-Recent-ISO.csv', index=False)
                        
                        st.sidebar.success("✅ Data processed and ready!")
                        
                    except Exception as e:
                        st.sidebar.error(f"❌ Error processing data: {e}")
    
    # Analysis Controls
    st.sidebar.markdown("### 📈 Analysis Settings")
    analysis_period = st.sidebar.selectbox(
        "Select Analysis Period:",
        ["Last 30 days", "Last 90 days", "Last 365 days", "All Time"],
        index=2
    )
    
    period_map = {
        "Last 30 days": 30,
        "Last 90 days": 90,
        "Last 365 days": 365,
        "All Time": None
    }
    days_filter = period_map[analysis_period]
    
    # Main Dashboard Content
    df = process_data()
    
    if df is None:
        st.error("No data available. Please update data from Google Sheets first.")
        return
    
    # Key Metrics
    st.markdown("## 📊 Key Metrics")
    
    if days_filter:
        cutoff_date = df['Date/Time'].max() - pd.Timedelta(days=days_filter)
        df_filtered = df[df['Date/Time'] >= cutoff_date]
    else:
        df_filtered = df
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🎵 Total Plays", f"{len(df_filtered):,}")
    
    with col2:
        st.metric("🎤 Unique Artists", df_filtered['Artist'].nunique())
    
    with col3:
        st.metric("🎶 Unique Songs", df_filtered['Song Name'].nunique())
    
    with col4:
        avg_daily = len(df_filtered) / (days_filter or ((df_filtered['Date/Time'].max() - df_filtered['Date/Time'].min()).days + 1))
        st.metric("📅 Avg Daily Plays", f"{avg_daily:.1f}")
    
    with col5:
        most_active_hour = df_filtered['Date/Time'].dt.hour.mode().iloc[0] if len(df_filtered) > 0 else 0
        st.metric("⏰ Most Active Hour", f"{most_active_hour}:00")
    
    # Charts
    st.markdown("## 📈 Listening Trends")
    
    # Time analysis
    fig_daily = create_time_analysis(df)
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # Top content
    st.markdown("## 🏆 Top Content")
    fig_artists, fig_songs = create_top_content_charts(df, days_filter)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_artists, use_container_width=True)
    with col2:
        st.plotly_chart(fig_songs, use_container_width=True)
    
    # Listening patterns
    st.markdown("## 🕰️ Listening Patterns")
    fig_hourly, fig_weekday = create_pattern_analysis(df, days_filter)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_hourly, use_container_width=True)
    with col2:
        st.plotly_chart(fig_weekday, use_container_width=True)
    
    # Data table
    st.markdown("## 🗂️ Raw Data")
    if st.checkbox("Show raw data"):
        st.dataframe(df_filtered.head(1000))
        st.caption("Showing first 1000 rows")

if __name__ == "__main__":
    main()
