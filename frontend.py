import streamlit as st
import pandas as pd
import requests

# Replace <username>/<repo> with your GitHub repo info
URL = "https://raw.githubusercontent.com/<username>/<repo>/main/reddit_posts.json"
data = requests.get(URL).json()
df = pd.DataFrame(data)

st.set_page_config(page_title="Reddit Nepal Dashboard", layout="wide")
st.markdown("## 🔥 Reddit Nepal Discussions")
st.markdown("---")

# Filters
col1, col2, col3 = st.columns([2,1,1])
with col1:
    keyword = st.text_input("🔍 Search by keyword")
with col2:
    sort_by = st.selectbox("Sort by", ["Newest", "Most Upvoted", "Most Commented"])
with col3:
    subreddit_filter = st.selectbox("Filter by Subreddit", ["All"] + df["subreddit"].unique().tolist())

filtered_df = df.copy()
if keyword:
    filtered_df = filtered_df[filtered_df["heading"].str.contains(keyword, case=False, na=False)]
if subreddit_filter != "All":
    filtered_df = filtered_df[filtered_df["subreddit"] == subreddit_filter]

if sort_by == "Most Upvoted":
    filtered_df = filtered_df.sort_values(by="upvotes", ascending=False)
elif sort_by == "Most Commented":
    filtered_df = filtered_df.sort_values(by="comment_counts", ascending=False)
else:
    filtered_df = filtered_df.sort_values(by="time_posted", ascending=False)

for _, row in filtered_df.iterrows():
    with st.container():
        st.markdown(f"""
            <div class="post-card">
                <h4>🔹 <a href="{row['url']}" target="_blank" class="post-link">{row['heading']}</a></h4>
                <p><i>📌 from r/{row['subreddit']}</i></p>
                <p>{row['body']}</p>
                <p class="metric-text">
                    ⬆️ <b>{row['upvotes']}</b> &nbsp;|&nbsp; 💬 <b>{row['comment_counts']}</b> &nbsp;|&nbsp; 📅 {row['time_posted']}
                </p>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("💭 View Comments"):
            for c in row["comments"].split("|||"):
                st.write(f"💬 {c}")

