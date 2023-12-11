import praw
import pandas as pd

class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent, username, password):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            check_for_async=False,
            username=username,
            password=password
        )
        self.reddit.read_only = True

    def search_posts(self, keywords, subreddit='depresion'):
        post_titles = []
        post_texts = []
        post_authors = []
        post_dates = []
        post_subreddits = []

        for keyword in keywords:
            search_results = self.reddit.subreddit(subreddit).search(keyword)

            for submission in search_results:
                if (keyword in submission.title.lower()) or (keyword in submission.selftext.lower()):
                    post_titles.append(submission.title)
                    post_texts.append(submission.selftext)
                    post_authors.append(submission.author.name if submission.author else "[Eliminado]")
                    post_dates.append(pd.to_datetime(submission.created_utc, unit='s'))
                    post_subreddits.append(submission.subreddit.display_name)

        data = {
            'title': post_titles,
            'post': post_texts,
            'username': post_authors,
            'date': post_dates,
            'subreddit': post_subreddits
        }

        return pd.DataFrame(data)