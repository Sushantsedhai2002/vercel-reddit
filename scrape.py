import praw
import json
from datetime import datetime, timedelta
from config import *

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

subreddits = ["Nepal", "technepal", "NepalSocial", "NepalPlusTwo"]

# Function to fetch posts for a given time filter
def fetch_posts(time_filter):
    posts_data = []
    for sub in subreddits:
        subreddit = reddit.subreddit(sub)

        # Decide which Reddit API call to use
        if time_filter == "day":
            posts = subreddit.hot(limit=30)
        else:
            top_filter = "week" if time_filter == "week" else "month"
            posts = subreddit.top(time_filter=top_filter, limit=30)

        for post in posts:
            post_time = datetime.fromtimestamp(post.created_utc)

            # Handle custom 14 days
            if time_filter == "14_days" and post_time < datetime.now() - timedelta(days=14):
                continue

            post.comments.replace_more(limit=0)
            comments = "|||".join([c.body.replace("\n", " ") for c in post.comments])

            posts_data.append({
                "subreddit": sub,
                "heading": post.title,
                "body": post.selftext.strip().replace("\n", " "),
                "upvotes": post.score,
                "time_posted": post_time.strftime('%Y-%m-%d %H:%M'),
                "comment_counts": post.num_comments,
                "comments": comments,
                "url": "https://www.reddit.com/" + post.permalink
            })
    return posts_data

# Fetch posts for all timeframes
all_data = {
    "day": fetch_posts("day"),
    "week": fetch_posts("week"),
    "14_days": fetch_posts("14_days"),
    "month": fetch_posts("month")
}

# Save to JSON
with open("reddit_posts.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print("Reddit posts updated successfully for all timeframes!")
