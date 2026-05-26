import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px

# Configuration
API_KEY = "AIzaSyCVJnWvkoLxmnYyqOM4EXEf8mDOV1mK2cY"  # <-- Paste your Google API Key here

# Initialize YouTube API Client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_stats(channel_id):
    """Fetches high-level stats for a given channel ID."""
    request = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        id="UC0IWRLai-BAwci_e9MylNGw"
        
    )
    response = request.execute()
    
    if not response.get('items'):
        return None
        
    item = response['items'][0]
    stats = {
        'title': item['snippet']['title'],
        'subscribers': int(item['statistics']['subscriberCount']),
        'views': int(item['statistics']['viewCount']),
        'total_videos': int(item['statistics']['videoCount']),
        'uploads_playlist': item['contentDetails']['relatedPlaylists']['uploads']
    }
    return stats

def get_video_list(uploads_playlist_id):
    """Retrieves the latest 50 video IDs from the uploads playlist."""
    video_ids = []
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_playlist_id,
        maxResults=50
    )
    response = request.execute()
    
    for item in response.get('items', []):
        video_ids.append(item['contentDetails']['videoId'])
        
    return video_ids

def get_video_details(video_ids):
    """Fetches metrics for a batch of video IDs."""
    video_data = []
    # API allows batching up to 50 IDs at once
    request = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    )
    response = request.execute()
    
    for item in response.get('items', []):
        stats = item.get('statistics', {})
        video_data.append({
            'Title': item['snippet']['title'],
            'Published At': pd.to_datetime(item['snippet']['publishedAt']),
            'Views': int(stats.get('viewCount', 0)),
            'Likes': int(stats.get('likeCount', 0)),
            'Comments': int(stats.get('commentCount', 0))
        })
        
    return pd.DataFrame(video_data)

# --- STREAMLIT UI ---
st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")
st.title("📊 YouTube Channel Analytics Dashboard")

# Input for Channel ID (Example default is MrBeast's channel ID)
channel_id = st.sidebar.text_input("Enter YouTube Channel ID:", value="UCX6OQ3DkcsbYNE6H8uQQuVA")

if channel_id:
    with st.spinner("Fetching data from YouTube..."):
        channel_info = get_channel_stats(channel_id)
        
        if channel_info:
            # Display Header Metrics
            st.header(f"Channel: {channel_info['title']}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Subscribers", f"{channel_info['subscribers']:,}")
            col2.metric("Total Lifetime Views", f"{channel_info['views']:,}")
            col3.metric("Total Videos Uploaded", f"{channel_info['total_videos']:,}")
            
            # Fetch and process video metrics
            video_ids = get_video_list(channel_info['uploads_playlist'])
            df = get_video_details(video_ids)
            
            if not df.empty:
                st.write("---")
                st.subheader("🚀 Recent Video Performance (Latest 50 Videos)")
                
                # Dynamic Charts using Plotly
                fig_views = px.bar(df, x='Title', y='Views', title="Views per Video", color='Views')
                st.plotly_chart(fig_views, use_container_width=True)
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    fig_likes = px.scatter(df, x='Views', y='Likes', size='Comments', hover_name='Title',
                                           title="Engagement: Views vs Likes (Size = Comments)")
                    st.plotly_chart(fig_likes, use_container_width=True)
                    
                with col_right:
                    # Top Performing Videos Dataframe
                    st.write("**Top 5 Most Viewed Recent Videos**")
                    top_5 = df.nlargest(5, 'Views')[['Title', 'Views', 'Likes']]
                    st.dataframe(top_5, use_container_width=True, hide_index=True)
            else:
                st.warning("No videos found or unable to fetch video data.")
        else:
            st.error("Could not find a channel with that ID. Double check the ID format.")