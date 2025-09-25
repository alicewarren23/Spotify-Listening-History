# 🎵 Spotify Listening History Dashboard

A beautiful, interactive web dashboard for analyzing your Spotify listening history data. This dashboard combines your Google Sheets data with powerful visualizations to provide insights into your music listening patterns.

## ✨ Features

- **📊 Real-time Data Updates**: Automatically fetch and process data from Google Sheets
- **📈 Interactive Visualizations**: Beautiful charts and graphs powered by Plotly
- **🕰️ Time-based Analysis**: View trends over different time periods (30 days, 90 days, 365 days, or all time)
- **🏆 Top Content Analysis**: See your most played songs and artists
- **⏰ Pattern Recognition**: Understand your listening habits by hour and day of week
- **📱 Responsive Design**: Works great on desktop and mobile devices
- **🎨 Spotify-themed UI**: Beautiful green color scheme matching Spotify's branding

## 🚀 Quick Start

### Option 1: Using the Launch Script (Easiest)
```bash
./launch_dashboard.sh
```

### Option 2: Manual Setup
1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the dashboard:
   ```bash
   streamlit run spotify_dashboard.py
   ```

3. Open your web browser and go to: `http://localhost:8501`

## 🔧 Prerequisites

- Python 3.7+
- pip3
- Your Google Sheets API credentials file (`lucid-parsec-464412-t8-75d0c2e2a5fa.json`)
- Access to your Spotify data in Google Sheets

## 📊 Dashboard Sections

### 1. Data Management
- **Update Data**: Fetch the latest data from your Google Sheets
- **Automatic Processing**: Combines historical and recent data, removes duplicates, and standardizes formats

### 2. Key Metrics
- Total plays for the selected period
- Unique artists and songs
- Average daily plays
- Most active listening hour

### 3. Listening Trends
- Daily activity with rolling averages
- Long-term patterns and trends

### 4. Top Content
- Most played artists and songs
- Customizable time periods

### 5. Listening Patterns
- Activity by hour of day
- Activity by day of week
- Discover your peak listening times

### 6. Raw Data View
- Browse your actual listening data
- Export capabilities

## 🎛️ Dashboard Controls

### Analysis Period Selection
Choose from:
- **Last 30 days**: Recent short-term trends
- **Last 90 days**: Medium-term patterns  
- **Last 365 days**: Annual overview (default)
- **All Time**: Complete listening history

### Data Updates
- Click "🔄 Update Data from Google Sheets" to refresh your data
- The system automatically processes and cleans the data
- Updates both historical and recent listening data

## 📁 File Structure

```
Spotify-Listening-History-1/
├── spotify_dashboard.py          # Main dashboard application
├── launch_dashboard.sh          # Easy startup script
├── requirements.txt             # Python dependencies
├── lucid-parsec-464412-t8-75d0c2e2a5fa.json  # Google Sheets API credentials
├── Transformation.ipynb         # Original data processing notebook
├── Exploratory-Analysis.ipynb   # Original analysis notebook
├── UTDSpotify_History.csv      # Main dataset
└── Archived_CSV/               # Historical data backups
```

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **Google Sheets API**: Data source integration

### Data Processing Pipeline
1. Fetches data from Google Sheets using gspread
2. Combines historical and recent datasets
3. Removes duplicates and cleans data
4. Standardizes date formats to ISO format
5. Creates processed dataset for analysis

### Visualization Features
- Interactive charts with zoom and hover
- Responsive design for all screen sizes
- Color-coded metrics and trends
- Export capabilities for charts
- Real-time data updates

## 🎨 Customization

The dashboard uses a Spotify-inspired color scheme with green (#1DB954) as the primary color. You can customize:

- Color schemes in the CSS section
- Chart types and styling
- Metrics and KPIs displayed
- Time period options
- Data filters and groupings

## 🔍 Troubleshooting

### Common Issues

1. **"No data available" error**
   - Make sure to click "Update Data from Google Sheets" first
   - Check that your credentials file is in the correct location

2. **Import errors**
   - Run `pip install -r requirements.txt` to install all dependencies
   - Make sure you're using Python 3.7+

3. **Google Sheets access issues**
   - Verify your credentials file is valid
   - Ensure your Google Sheets are named correctly:
     - "Spotify History" for historical data
     - "Recent Spotify Plays" for recent data

4. **Performance issues**
   - Large datasets may take time to process
   - Consider filtering to shorter time periods for faster loading

## 📈 Data Sources

The dashboard expects data from two Google Sheets:
- **"Spotify History"**: Your historical listening data
- **"Recent Spotify Plays"**: Your recent listening data

Data should include columns:
- Date/Time
- Song Name
- Artist
- Song ID (optional)
- URI (automatically removed during processing)

## 🔮 Future Enhancements

Potential improvements:
- Genre analysis and classification
- Mood and energy level tracking
- Playlist analysis
- Social sharing features
- Export to various formats
- Advanced statistical analysis
- Machine learning recommendations

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure your Google Sheets data format matches expectations
4. Check the console/terminal for detailed error messages

---

**Enjoy exploring your Spotify listening history! 🎵**
