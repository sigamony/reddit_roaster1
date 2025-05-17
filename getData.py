import praw
import os
from dotenv import load_dotenv

# 🔑 Reddit API Credentials (Replace these with yours)

# load_dotenv()
# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# USER_AGENT = os.getenv("USER_AGENT")

CLIENT_ID = "n9qQrhArDFOh6ar4dOZTGA"
CLIENT_SECRET = "a4h3G8rjaRAxiKybJJccxXAXkeq9Hw"
USER_AGENT = "reddit-roaster-script:v1.0 (by /u/l0g1cb0mb_101)"


# Initialize PRAW
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

def get_user_data(username, post_limit=10, comment_limit=15):
    posts = []
    comments = []
    
    try:
        user = reddit.redditor(username)

        # Get posts
        for submission in user.submissions.new(limit=post_limit):
            posts.append({
                'title': submission.title,
                'selftext': submission.selftext,
                'subreddit': submission.subreddit.display_name,
                'url': submission.url
            })

        # Get comments
        for comment in user.comments.new(limit=comment_limit):
            comments.append({
                'body': comment.body,
                'subreddit': comment.subreddit.display_name
            })

    except Exception as e:
        print(f"Error fetching data: {e}")
    
    return posts, comments

def build_llm_prompt(username, posts, comments):
    prompt = f"Roast the Reddit user '{username}' based on their online activity. " \
             "Below you will find a list of their recent posts and comments. " \
             "Use this information to write a humorous and scathingly witty roast that plays off the user's username and the tone of their contributions.\n\n"
    
    prompt += "Posts:\n"
    for idx, post in enumerate(posts, start=1):
        prompt += f"{idx}. Title: {post['title']}\n"
        if post['selftext']:
            prompt += f"   Content: {post['selftext']}\n"
        prompt += f"   Subreddit: {post['subreddit']}\n"
        prompt += f"   URL: {post['url']}\n\n"
    
    prompt += "Comments:\n"
    for idx, comment in enumerate(comments, start=1):
        prompt += f"{idx}. Subreddit: {comment['subreddit']}\n"
        prompt += f"   Comment: {comment['body']}\n\n"
    
    prompt += "Now, based on the above information, write a roast that humorously critiques the user."
    return prompt

# Run the script
if __name__ == "__main__":
    username = input("Enter the Reddit username: ").strip()
    posts, comments = get_user_data(username)

    if posts or comments:
        prompt = build_llm_prompt(username, posts, comments)
        print("\n=== LLM Prompt ===\n")
        print(prompt)
    else:
        print("No data found for the specified user.")
