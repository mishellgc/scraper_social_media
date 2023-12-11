import pandas as pd

def integrate_data(data_twitter, data_reddit, data_tumblr):
    # data_twitter
    data_twitter = pd.DataFrame(data_twitter, columns=['username', 'handle', 'date', 'text','reply_text', 'reply_cnt', 'retweet_cnt', 'like_cnt'])
    data_twitter['post'] = data_twitter.apply(lambda row: row.reply_text if 'Replying to' in row.text else row.text, axis=1)
    data_twitter['date'] = pd.to_datetime(data_twitter.date)
    data_twitter['red_social'] = "twitter"

    # data_reddit
    data_reddit['date'] = pd.to_datetime(data_reddit.date)
    data_reddit['red_social'] = "reddit"

    # data_tumblr
    data_tumblr['date'] = pd.to_datetime(data_tumblr.date)
    data_tumblr['red_social'] = "tumblr"
    data_tumblr = data_tumblr.rename(columns={'blog_name':'username','summary':'post'})

    integrated_data = pd.concat([data_twitter[['username','date','post','red_social']],
                                 data_reddit[['username','date','post','red_social']],
                                 data_tumblr[['username','date','post','red_social']]])
    
    return integrated_data
