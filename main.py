from social_media_scraper.twitter_scraper import TwitterScraper
from social_media_scraper.reddit_scraper import RedditScraper
from social_media_scraper.tumblr_scraper import TumblrScraper
from social_media_scraper.data_integration import integrate_data
from social_media_scraper.database import connect_to_mongodb, insert_data_to_mongodb

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Configuración y palabras clave
issue = 'depresion'
keywords = ['agobiado', 'agobiada', 'agotado', 'agotada', 'angustiado', 'angustiada', 'ansiedad', 'ansioso', 'ansiosa',
            'cansado', 'cansada', 'decaído', 'depresión', 'depresion', 'depresivo', 'depresiva', 'deprimido', 'deprimida',
            'desanimado', 'desanimada', 'desesperado', 'desesperada', 'desmotivado', 'desmotivada', 'insomnio', 'llorar',
            'nervioso', 'preocupado', 'preocupada', 'triste', 'vacío', 'vacía']


# Configuración de credenciales
twitter_email = os.getenv("TWITTER_EMAIL")
twitter_username = os.getenv("TWITTER_USERNAME")
twitter_password = os.getenv("TWITTER_PASSWORD")

reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_user_agent = os.getenv("REDDIT_USER_AGENT")
reddit_username = os.getenv("REDDIT_USERNAME")
reddit_password = os.getenv("REDDIT_PASSWORD")

tumblr_consumer_key = os.getenv("TUMBLR_CONSUMER_KEY")
tumblr_oauth_token = os.getenv("TUMBLR_OAUTH_TOKEN")
tumblr_oauth_secret = os.getenv("TUMBLR_OAUTH_SECRET")


# Configuración de credenciales MongoDB Atlas
mongodb_username = os.getenv("MONGODB_USERNAME")
mongodb_password = os.getenv("MONGODB_PASSWORD")
mongodb_cluster = os.getenv("MONGODB_CLUSTER")
mongodb_uri = 'mongodb+srv://'+mongodb_username+':'+mongodb_password+'@'+mongodb_cluster+'.ksltkoi.mongodb.net/'

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Inicialización y ejecución del scraper de Twitter
twitter_scraper = TwitterScraper(twitter_email,
                                 twitter_username,
                                 twitter_password)
data_twitter = twitter_scraper.run()

# Inicialización y ejecución del scraper de Reddit
reddit_scraper = RedditScraper(reddit_client_id,
                        reddit_client_secret,
                        reddit_user_agent,
                        reddit_username,
                        reddit_password)
data_reddit = reddit_scraper.search_posts(keywords)

# Inicialización y ejecución del scraper de Tumblr
tumblr_scraper = TumblrScraper( tumblr_consumer_key,
                                tumblr_oauth_token,
                                tumblr_oauth_secret,
                                palabras_clave=keywords)
data_tumblr = tumblr_scraper.scrape_posts()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Integración de datos
integrated_data = integrate_data(data_twitter, data_reddit, data_tumblr)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Conexión a MongoDB
client, db = connect_to_mongodb(mongodb_uri)

# Insertar datos en MongoDB
collection_name = 'data_raw'
insert_data_to_mongodb(db, collection_name, integrated_data)

# Cerrar la conexión a MongoDB
client.close()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#