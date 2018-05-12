# Get today's date
import datetime

# Time interval between tweets
import time

# For interfacing with Twitter
import tweepy

# Import parse object script
import parse_object

# Import our Twitter credentials from credentials.py
from twitter_credentials import *

# Import Twitter media upload script
import twitter_media_upload

# Import json to transform media json string to dictionary
import json

# Adding a random factor to the Tweet timing
import random

# For writing output to file
import sys

# User agent for downloading images
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#  Get today's date
year_today = datetime.date.today().strftime("%Y")
month_today = datetime.date.today().strftime("%B")
month_number_today = datetime.date.today().strftime("%m")
day_today = datetime.date.today().strftime("%-d")
day_full_today = datetime.date.today().strftime("%d")

# Get today's posts from parse server
posts = parse_object.get_posts(month_today, day_today)

# Open log file
sys.stdout = open("./outputs/" + year_today + month_number_today
                  + day_full_today + ".txt", "w")

# Tweet every hour
def tweet():

    count = 1

    for post in posts:
        print ''
        print ''
        print ''
        print "Tweet " + str(count)

        # Get media file locations in a list
        images = []
        media_dict = json.loads(post.media)
        for key in media_dict:
            image = list(media_dict[key])
            for index in range(len(image)):
                if image[index:index+3] == ['%', '2', '0']:
                    image[index:index+3] = [' ', '', '']
            images.append('../' + ''.join(image))
        print ''
        print "Image list: " + str(images)
        print ''

        tweeted = False
        tweet_fail_count = 0

        # Randomly choose an image and try to tweet
        while (tweeted == False and tweet_fail_count < 20):
            # Randomly choose image
            media_id_list = []
            image = random.choice(images)
            print ''
            print "Randomly selected image: " + str(image)
            print ''

            # Upload chosen image
            image_object = twitter_media_upload.ImageTweet(image)
            try:
                image_object.upload_init()
                image_object.upload_append()
                image_object.upload_finalize()
                media_id_list.append(image_object.media_id)
            except KeyError:
                print "KeyError"
            print ''
            print "media_id_list: " + str(media_id_list)
            print ''

            # Make Tweet
            year_diff = int(year_today) - int(post.year)
            try:
                 if post.title != '':
                     text = str(year_diff) + 'YOUR_TWEET_TEXT'
                     api.update_status(status = text, media_ids = media_id_list)
                     print "Tweet " \
                           + str(count) \
                           + " succeeded on " \
                           + str(datetime.datetime.now())
                     tweeted = True
                     time.sleep(random.randint(3600, 7200))
                 else:
                    pass
            except tweepy.TweepError as e:
                print(e.reason)
                print "Tweet "\
                      + str(count) \
                      + " failed on " \
                      + str(datetime.datetime.now())

        count += 1
        print ''
        print ''
        print ''
        print "---------------------------------------------------------------"

# Delay of initial tweet
time.sleep(random.randint(0,600))
tweet()

sys.stdout.close()
