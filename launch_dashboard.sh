#!/bin/bash

# Spotify Dashboard Launcher Script

echo "🎵 Starting Spotify Listening History Dashboard..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 to continue."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 to continue."
    exit 1
fi

# Install requirements if they don't exist
echo "📦 Installing required packages..."
pip3 install -r requirements.txt

# Check if streamlit is installed successfully
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit installation failed. Please check your Python environment."
    exit 1
fi

# Launch the dashboard
echo "🚀 Launching dashboard..."
echo "📱 The dashboard will open in your default web browser."
echo "🛑 Press Ctrl+C to stop the dashboard server."
echo ""

streamlit run spotify_dashboard.py
