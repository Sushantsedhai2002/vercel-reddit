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

posts_data = []

for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    posts = subreddit.top(time_filter="day", limit=30) 

    for post in posts:
        post_time = datetime.fromtimestamp(post.created_utc)
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

# Save to JSON
with open("reddit_posts.json", "w", encoding="utf-8") as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=4)

print("Reddit posts updated successfully!")
