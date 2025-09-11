import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ---------------------- Configuration ------------------------
st.set_page_config(
    page_title="Reddit Nepal Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# GitHub raw JSON URL
URL = "https://raw.githubusercontent.com/Sushantsedhai2002/vercel-reddit/main/reddit_posts.json"

# ---------------------- Enhanced CSS Styling ----------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        .main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        .dashboard-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 20px; margin-bottom: 2rem; text-align: center; color: white; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); }
        .dashboard-title { font-family: 'Inter', sans-serif; font-size: 2.5rem; font-weight: 700; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .dashboard-subtitle { font-family: 'Inter', sans-serif; font-size: 1.1rem; font-weight: 300; margin-top: 0.5rem; opacity: 0.9; }
        .stats-container { background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); margin-bottom: 2rem; border-left: 5px solid #667eea; }
        .stat-item { display: inline-block; margin-right: 2rem; font-family: 'Inter', sans-serif; }
        .stat-number { font-size: 1.8rem; font-weight: 700; color: #667eea; }
        .stat-label { font-size: 0.9rem; color: #666; font-weight: 500; }
        .filter-section { background: #f8fafc; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; border: 1px solid #e2e8f0; }
        .post-card { background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%); padding: 1.8rem; border-radius: 18px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); margin-bottom: 1.5rem; border: 1px solid #e2e8f0; transition: all 0.3s ease; font-family: 'Inter', sans-serif; }
        .post-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.12); border-color: #667eea; }
        .post-title { font-size: 1.3rem; font-weight: 600; margin-bottom: 0.8rem; line-height: 1.4; }
        .post-link { text-decoration: none; color: #1a202c; transition: color 0.2s ease; }
        .post-link:hover { color: #667eea; text-decoration: none; }
        .post-meta { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; font-size: 0.9rem; color: #667eea; font-weight: 500; }
        .subreddit-badge { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }
        .post-body { color: #4a5568; line-height: 1.6; margin-bottom: 1.2rem; font-size: 0.95rem; }
        .post-stats { display: flex; align-items: center; gap: 1.5rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; font-size: 0.9rem; color: #718096; }
        .stat-item-post { display: flex; align-items: center; gap: 0.3rem; font-weight: 500; }
        .stat-value { color: #2d3748; font-weight: 600; }
        .comment-section { background: #f7fafc; border-radius: 12px; padding: 1rem; margin-top: 1rem; }
        .comment-item { background: white; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #667eea; font-size: 0.9rem; line-height: 1.5; }
        .last-updated { background: linear-gradient(45deg, #48bb78, #38a169); color: white; padding: 0.5rem 1rem; border-radius: 25px; font-size: 0.85rem; font-weight: 500; display: inline-block; margin-bottom: 1rem; }
        .stSpinner > div { border-top-color: #667eea !important; }
        .no-results { text-align: center; padding: 3rem; color: #718096; font-size: 1.1rem; }
        @media (max-width: 768px) {
            .dashboard-title { font-size: 2rem; }
            .post-card { padding: 1.2rem; }
            .post-stats { flex-wrap: wrap; gap: 1rem; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------- Load Data with Spinner ----------------------
@st.cache_data(ttl=3600)
def load_data():
    response = requests.get(URL)
    data = response.json()  # {'day':[...], 'week':[...], '14_days':[...], 'month':[...]}
    last_updated = datetime.now()
    return data, last_updated

with st.spinner("⏳ Fetching latest Reddit posts..."):
    data, last_updated = load_data()

# ---------------------- Sidebar: Timeframe ----------------------
timeframe_choice = st.sidebar.selectbox(
    "Select Timeframe",
    ["day", "week", "14_days", "month"],
    format_func=lambda x: {"day":"Last 24h", "week":"Last 7 Days", "14_days":"Last 14 Days", "month":"Last Month"}[x]
)

# Convert selected timeframe to DataFrame
df = pd.DataFrame(data[timeframe_choice])
df['time_posted'] = pd.to_datetime(df['time_posted'])

# ---------------------- Dashboard Header ----------------------
st.markdown(f"""
    <div class="dashboard-header">
        <h1 class="dashboard-title">🇳🇵 Reddit Nepal Dashboard</h1>
        <p class="dashboard-subtitle">Showing posts from <b>{timeframe_choice.replace('_',' ').title()}</b></p>
    </div>
""", unsafe_allow_html=True)

# ---------------------- Stats Section ----------------------
total_posts = len(df)
total_upvotes = df['upvotes'].sum()
total_comments = df['comment_counts'].sum()
unique_subreddits = df['subreddit'].nunique()

st.markdown(f"""
    <div class="stats-container">
        <div class="stat-item">
            <div class="stat-number">{total_posts:,}</div>
            <div class="stat-label">Total Posts</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_upvotes:,}</div>
            <div class="stat-label">Total Upvotes</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_comments:,}</div>
            <div class="stat-label">Total Comments</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{unique_subreddits}</div>
            <div class="stat-label">Subreddits</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Last Updated Badge
st.markdown(f"""
    <div class="last-updated">
        🔄 Last Updated: {last_updated.strftime('%B %d, %Y at %H:%M:%S')}
    </div>
""", unsafe_allow_html=True)

# ---------------------- Filters ----------------------
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown("### 🔧 **Filter & Sort Options**")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    keyword = st.text_input("🔍 Search by keyword", placeholder="Enter keywords to search in post titles...")
with col2:
    sort_by = st.selectbox("📊 Sort by", ["Newest", "Most Upvoted", "Most Commented"], help="Choose how to sort the posts")
with col3:
    subreddit_filter = st.selectbox("📌 Filter by Subreddit", ["All"] + sorted(df["subreddit"].unique().tolist()), help="Filter posts by specific subreddit")

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
    st.markdown(f"**📊 Showing {len(filtered_df)} of {len(df)} posts**")
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
                        <a href="{row['url']}" target="_blank" class="post-link">{row['heading']}</a>
                    </div>
                    <div class="post-body">{body_text}</div>
                    <div class="post-stats">
                        <div class="stat-item-post">⬆️ <span class="stat-value">{row['upvotes']:,}</span> upvotes</div>
                        <div class="stat-item-post">💬 <span class="stat-value">{row['comment_counts']:,}</span> comments</div>
                        <div class="stat-item-post">🔗 <a href="{row['url']}" target="_blank" style="color: #667eea; text-decoration: none;">View on Reddit</a></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if row["comments"] and str(row["comments"]) != "nan":
                with st.expander(f"💭 View Comments ({row['comment_counts']} total)"):
                    st.markdown('<div class="comment-section">', unsafe_allow_html=True)
                    comments = str(row["comments"]).split("|||")
                    for comment in comments:
                        if comment.strip():
                            st.markdown(f'<div class="comment-item">💬 {comment.strip()}</div>', unsafe_allow_html=True)


# ---------------------- Footer ----------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;'>
        <p>🚀 Built with Streamlit | 📊 Data refreshed every hour | 🇳🇵 Made for Nepal Reddit Community</p>
    </div>
""", unsafe_allow_html=True)
