# 📊 YouTube Channel Analytics Dashboard

A lightweight, real-time analytics dashboard built with Python that interacts directly with Google's official YouTube Data API v3. This application allows users to fetch comprehensive channel metrics and visualize recent video performance dynamically.

## 🚀 Features
- **Real-Time Channel Metrics:** Fetches live data including total subscribers, lifetime views, and total video uploads for any specific YouTube Channel ID.
- **Video Performance Tracking:** Automatically pulls stats for the latest 50 video uploads.
- **Interactive Visualizations:** Features interactive Plotly charts tracking views per video and user engagement metrics (Views vs. Likes weighted by comment volume).
- **Data Insights:** Renders top-performing video highlights instantly into a clean data frame.

## 🛠️ Tech Stack
- **Language:** Python
- **API Integration:** Google API Python Client (YouTube Data API v3)
- **Frontend/UI:** Streamlit
- **Data Manipulation:** Pandas
- **Data Visualization:** Plotly Express

## 📦 Installation & Setup
1. Clone the repository and install dependencies:
```bash
   pip install google-api-python-client streamlit pandas plotly
