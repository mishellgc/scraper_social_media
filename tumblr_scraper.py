import requests
import pandas as pd

class TumblrScraper:
    BASE_URL = "https://api.tumblr.com/v2/tagged"

    def __init__(self, consumer_key, oauth_token, oauth_secret, palabras_clave):
        self.credentials = {
            "api_key": consumer_key,
            "oauth_token": oauth_token,
            "oauth_secret": oauth_secret,
        }
        self.palabras_clave = palabras_clave

    def scrape_posts(self, limit_per_tag=10000):
        all_posts = []

        for hashtag in self.palabras_clave:
            offset = 0

            while True:
                posts = self._get_tagged_posts(hashtag, offset, limit_per_tag)

                if not posts:
                    break

                all_posts.extend(posts)
                offset += limit_per_tag
        
        data = pd.DataFrame(all_posts)
        return data

    def _get_tagged_posts(self, hashtag, offset, limit):
        params = {
            "tag": hashtag,
            **self.credentials,
            "offset": offset,
            "limit": limit,
        }
        response = requests.get(self.BASE_URL, params=params)
        
        if response.status_code == 200:
            return response.json().get("response", [])
        else:
            print(f"Error al buscar el hashtag '{hashtag}': {response.status_code}")
            return []
