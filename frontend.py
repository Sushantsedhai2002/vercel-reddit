import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ---------------------- Configuration ----------------------
st.set_page_config(
    page_title="Reddit Nepal Dashboard", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# GitHub raw JSON URL
URL = "https://raw.githubusercontent.com/Sushantsedhai2002/vercel-reddit/main/reddit_posts.json"

# ---------------------- Load Data with Spinner ----------------------
@st.cache_data(ttl=3600)
def load_data():
    response = requests.get(URL)
    data = response.json()
    
    # Convert time_posted to datetime for each timeframe
    for timeframe in data:
        for post in data[timeframe]:
            post["time_posted"] = datetime.strptime(post["time_posted"], '%Y-%m-%d %H:%M')
    last_updated = datetime.now()
    return data, last_updated

with st.spinner("⏳ Fetching latest Reddit posts..."):
    all_data, last_updated = load_data()

# ---------------------- Dashboard Header ----------------------
st.markdown(f"""
    <div class="dashboard-header">
        <h1 class="dashboard-title">🇳🇵 Reddit Nepal Dashboard</h1>
        <p class="dashboard-subtitle">Stay updated with the latest discussions from Nepali Reddit communities</p>
    </div>
""", unsafe_allow_html=True)

# Last Updated Badge
st.markdown(f"""
    <div class="last-updated">
        🔄 Last Updated: {last_updated.strftime('%B %d, %Y at %H:%M:%S')}
    </div>
""", unsafe_allow_html=True)

# ---------------------- Sidebar Filters ----------------------
with st.sidebar:
    st.header("⚙️ Settings")

    # Timeframe selector
    timeframe_choice = st.selectbox(
        "Select Timeframe",
        ["day", "week", "14_days", "month"],
        format_func=lambda x: {"day":"Last 24h", "week":"Last 7 Days", "14_days":"Last 14 Days", "month":"Last Month"}[x]
    )

# ---------------------- Convert JSON to DataFrame ----------------------
df = pd.DataFrame(all_data[timeframe_choice])

# ---------------------- Filters Section ----------------------
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown("### 🔧 **Filter & Sort Options**")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    keyword = st.text_input(
        "🔍 Search by keyword", 
        placeholder="Enter keywords to search in post titles..."
    )

with col2:
    sort_by = st.selectbox(
        "📊 Sort by", 
        ["Newest", "Most Upvoted", "Most Commented"],
        help="Choose how to sort the posts"
    )

with col3:
    subreddit_filter = st.selectbox(
        "📌 Filter by Subreddit", 
        ["All"] + sorted(df["subreddit"].unique().tolist()),
        help="Filter posts by specific subreddit"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- Filter & Sort Data ----------------------
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

# ---------------------- Results Info ----------------------
if len(filtered_df) != len(df):
    st.markdown(f"**📊 Showing {len(filtered_df)} of {len(df)} posts for {timeframe_choice}**")

st.markdown("---")

# ---------------------- Display Posts ----------------------
if len(filtered_df) == 0:
    st.markdown("""
        <div class="no-results">
            <h3>🔍 No posts found</h3>
            <p>Try adjusting your search criteria or filters</p>
        </div>
    """, unsafe_allow_html=True)
else:
    for _, row in filtered_df.iterrows():
        with st.container():
            # Truncate body text if too long
            body_text = row['body']
            if len(body_text) > 300:
                body_text = body_text[:300] + "..."

            st.markdown(f"""
                <div class="post-card">
                    <div class="post-meta">
                        <span class="subreddit-badge">r/{row['subreddit']}</span>
                        <span>📅 {row['time_posted'].strftime('%B %d, %Y at %H:%M')}</span>
                    </div>

                    <div class="post-title">
                        <a href="{row['url']}" target="_blank" class="post-link">
                            {row['heading']}
                        </a>
                    </div>

                    <div class="post-body">
                        {body_text}
                    </div>

                    <div class="post-stats">
                        <div class="stat-item-post">
                            <span>⬆️</span>
                            <span class="stat-value">{row['upvotes']:,}</span>
                            <span>upvotes</span>
                        </div>
                        <div class="stat-item-post">
                            <span>💬</span>
                            <span class="stat-value">{row['comment_counts']:,}</span>
                            <span>comments</span>
                        </div>
                        <div class="stat-item-post">
                            <span>🔗</span>
                            <a href="{row['url']}" target="_blank" style="color: #667eea; text-decoration: none;">
                                View on Reddit
                            </a>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Comments section
            if row["comments"] and str(row["comments"]) != "nan":
                with st.expander(f"💭 View Comments ({row['comment_counts']} total)"):
                    st.markdown('<div class="comment-section">', unsafe_allow_html=True)

                    comments = str(row["comments"]).split("|||")
                    for i, comment in enumerate(comments[:10]):  # Limit to first 10 comments
                        if comment.strip():
                            st.markdown(f"""
                                <div class="comment-item">
                                    💬 {comment.strip()}
                                </div>
                            """, unsafe_allow_html=True)

                    if len(comments) > 10:
                        st.markdown(f"<p style='text-align: center; color: #666; font-style: italic;'>... and {len(comments) - 10} more comments</p>", unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- Footer ----------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;'>
        <p>🚀 Built with Streamlit | 📊 Data refreshed every hour | 🇳🇵 Made for Nepal Reddit Community</p>
    </div>
""", unsafe_allow_html=True)
