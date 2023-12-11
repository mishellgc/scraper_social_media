import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class Tweet:
    def __init__(self, card):
        self.card = card

    def get_username(self):
        return self.card.find_element(By.XPATH, './/span').text

    def get_handle(self):
        return self.card.find_element(By.XPATH, './/span[contains(text(), "@")]').text

    def get_date(self):
        return self.card.find_element(By.XPATH, './/time').get_attribute('datetime')

    def get_post(self):
        return self.card.find_element(By.XPATH, './/div[1]/div[1]/div[2]/div[2]/div[2]').text
    
    def get_reply_post(self):
        return self.card.find_element(By.XPATH, './/div[1]/div[1]/div[2]/div[2]/div[3]').text
    
    def get_reply_count(self):
        return self.card.find_element(By.XPATH, './/div[@data-testid="reply"]').text

    def get_retweet_count(self):
        return self.card.find_element(By.XPATH, './/div[@data-testid="retweet"]').text

    def get_like_count(self):
        return self.card.find_element(By.XPATH, './/div[@data-testid="like"]').text

    def get_tweet_data(self):
        username = self.get_username()
        handle = self.get_handle()
        try:
            date = self.get_date()
        except NoSuchElementException:
            return None
        post = self.get_post()
        reply_post = self.get_reply_post()
        reply_cnt = self.get_reply_count()
        retweet_cnt = self.get_retweet_count()
        like_cnt = self.get_like_count()
        tweet = [username, handle, date, post, reply_post, reply_cnt, retweet_cnt, like_cnt]
        return tweet

    
class TwitterScraper:
    def __init__(self, email, username, password):
        self.url_social_media = "https://www.twitter.com/login"
        self.email_input = email
        self.username_input = username
        self.password_input = password
        self.driver = webdriver.Edge()

    def login(self):
        self.driver.get(self.url_social_media)
        self.driver.maximize_window()
        sleep(3)
        self._find_element_and_send_keys('//input[@name="text"]', self.email_input, submit=True)
        self._find_element_and_send_keys('//input[@name="text"]', self.username_input, submit=True)
        self._find_element_and_send_keys('//input[@name="password"]', self.password_input, submit=True)
        sleep(3)

    def search_tweets(self, issue, keywords):
        self._find_element_and_send_keys('//input[@aria-label="Search query"]', issue, submit=True)
        self._find_element_and_click('//div[@aria-label="More"]')
        self._find_element_and_click('.//span[contains(text(), "Advanced search")]')
        sleep(2)
        keys_search = ' '.join(keywords)
        self._find_element_and_send_keys('//input[@name="anyOfTheseWords"]', keys_search)
        sleep(2)
        self._select_option_by_visible_text('//select[@data-testid=""]', "Spanish")
        
        self._find_element_and_click('.//span[contains(text(), "Search")]')
        self._find_element_by_link_text_and_click('Latest')
        sleep(3)

    def scrape_tweets(self):
        data = []
        tweet_ids = set()
        last_position = self.driver.execute_script("return window.pageYOffset;")
        scrolling = True

        while scrolling:
            page_cards = self.driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

            for card in page_cards[-15:]:
                tweet_obj = Tweet(card)
                tweet = tweet_obj.get_tweet_data()
                if tweet:
                    tweet_id = ''.join(tweet)
                    if tweet_id not in tweet_ids:
                        tweet_ids.add(tweet_id)
                        data.append(tweet)

            scroll_attempt = 0

            while True:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(2)
                curr_position = self.driver.execute_script("return window.pageYOffset;")

                if last_position == curr_position:
                    scroll_attempt += 1
                    if scroll_attempt >= 3:
                        scrolling = False
                        break
                    else:
                        sleep(7)
                else:
                    last_position = curr_position
                    break

        return data

    def run_scraper(self, issue, keywords):
        self.login()
        self.search_tweets(issue, keywords)
        tweet_data = self.scrape_tweets()
        return tweet_data

    def _find_element_and_send_keys(self, xpath, keys, submit=False):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element.send_keys(keys)
        if submit:
            element.send_keys(Keys.ENTER)

    def _find_element_and_click(self, xpath):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()

    def _select_option_by_visible_text(self, xpath, text):
        select_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        select = Select(select_element)
        select.select_by_visible_text(text)
        
    def _find_element_by_link_text_and_click(self, link_text):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
        element.click()