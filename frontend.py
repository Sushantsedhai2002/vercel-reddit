import streamlit as st
import json
import pandas as pd
from datetime import datetime

# Load all JSON data (day, week, 14 days, month)
with open("reddit_posts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

st.set_page_config(page_title="Reddit Dashboard", layout="wide")

st.title("📊 Reddit Posts Dashboard")

# Last updated timestamp
last_updated = data.get("last_updated", None)
if last_updated:
    st.caption(f"⏱️ Last updated: {last_updated}")

# Timeframe selector
timeframe = st.selectbox("📅 Select Timeframe", ["day", "week", "14days", "month"])

# Subreddit filter
all_subreddits = sorted({p["subreddit"] for tf in data.values() for p in tf})
subreddit_filter = st.selectbox("📌 Filter by Subreddit", ["All"] + all_subreddits)

# Load posts for selected timeframe
posts = data.get(timeframe, [])

if subreddit_filter != "All":
    posts = [p for p in posts if p["subreddit"] == subreddit_filter]

if not posts:
    st.warning("No posts available for this selection.")
else:
    # Convert to DataFrame
    df = pd.DataFrame(posts)

    # Display summary stats
    st.subheader("📈 Summary Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Posts", len(df))
    col2.metric("Total Comments", df["comment_counts"].sum())
    col3.metric("Avg Upvotes", round(df["upvotes"].mean(), 2) if not df.empty else 0)

    # Table of posts
    st.subheader("📰 Posts")
    for _, row in df.iterrows():
        with st.expander(f"🔗 {row['heading']}"):
            st.write(f"**Subreddit:** {row['subreddit']}")
            st.write(f"👍 Upvotes: {row['upvotes']} | 💬 Comments: {row['comment_counts']}")
            st.write(f"🕒 Posted: {row['time_posted']}")
            if row['body']:
                st.write(f"📄 {row['body']}")
            st.markdown(f"[View Post]({row['url']})")

            # Show comments
            if row.get("comments"):
                st.markdown("**💬 Comments:**")
                for c in row["comments"].split("|||"):
                    st.markdown(f"- {c.strip()}")

    # Download button
    st.download_button(
        "⬇️ Download Posts Data",
        data=json.dumps(posts, indent=2),
        file_name=f"reddit_posts_{timeframe}.json",
        mime="application/json"
    )
