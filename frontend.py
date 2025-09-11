import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Reddit Nepal Dashboard", layout="wide")

URL = "https://raw.githubusercontent.com/Sushantsedhai2002/vercel-reddit/main/reddit_posts.json"

st.markdown(
    """
    <style>
        .post-card { background-color:#f9f9f9;padding:18px;border-radius:12px;
                     box-shadow:0px 2px 6px rgba(0,0,0,0.08);margin-bottom:18px; }
        .metric-text { font-size:16px;color:#555; }
        a.post-link { text-decoration:none;color:black;font-weight:bold; }
        a.post-link:hover { text-decoration:underline; }
    </style>
    """, unsafe_allow_html=True
)

@st.cache_data(ttl=3600)
def load_data():
    data = requests.get(URL).json()
    df = pd.DataFrame(data)
    df['time_posted'] = pd.to_datetime(df['time_posted'])
    return df

df = load_data()

st.markdown("## 🔥 Reddit Nepal Discussions")
st.markdown("---")

# Filters
col1, col2, col3 = st.columns([2,1,1])
with col1: keyword = st.text_input("🔍 Search by keyword")
with col2: sort_by = st.selectbox("Sort by", ["Newest", "Most Upvoted", "Most Commented"])
with col3: subreddit_filter = st.selectbox("Filter by Subreddit", ["All"] + df["subreddit"].unique().tolist())

filtered_df = df.copy()
if keyword: filtered_df = filtered_df[filtered_df["heading"].str.contains(keyword, case=False, na=False)]
if subreddit_filter != "All": filtered_df = filtered_df[filtered_df["subreddit"] == subreddit_filter]

if sort_by == "Most Upvoted": filtered_df = filtered_df.sort_values(by="upvotes", ascending=False)
elif sort_by == "Most Commented": filtered_df = filtered_df.sort_values(by="comment_counts", ascending=False)
else: filtered_df = filtered_df.sort_values(by="time_posted", ascending=False)

for _, row in filtered_df.iterrows():
    with st.container():
        st.markdown(f"""
            <div class="post-card">
                <h4>🔹 <a href="{row['url']}" target="_blank" class="post-link">{row['heading']}</a></h4>
                <p><i>📌 from r/{row['subreddit']}</i></p>
                <p>{row['body']}</p>
                <p class="metric-text">
                    ⬆️ <b>{row['upvotes']}</b> &nbsp;|&nbsp; 💬 <b>{row['comment_counts']}</b> &nbsp;|&nbsp; 📅 {row['time_posted'].strftime('%Y-%m-%d %H:%M')}
                </p>
            </div>
        """, unsafe_allow_html=True)
        with st.expander("💭 View Comments"):
            for c in row["comments"].split("|||"): st.write(f"💬 {c}")
