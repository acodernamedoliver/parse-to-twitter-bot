# OS independency
import os
# For exiting
import sys
# For controlling execution
import time

# Requests data from the web
import requests
# Twitter authentication
from requests_oauthlib import OAuth1

# Import our Twitter credentials from credentials.py
from twitter_credentials import *

# Destination for Twitter media
media_endpoint_url = 'https://upload.twitter.com/1.1/media/upload.json'
post_tweet_url = 'https://api.twitter.com/1.1/statuses/update.json'

oauth = OAuth1(consumer_key,
               client_secret=consumer_secret,
               resource_owner_key=access_token,
               resource_owner_secret=access_token_secret)

class ImageTweet(object):
    def __init__(self, file_name):
        '''
        Defines image tweet properties
        '''
        self.image_filename = file_name
        self.total_bytes = os.path.getsize(self.image_filename)
        self.media_id = None
        self.processing_info = None

    def upload_init(self):
        '''
        Initializes Upload
        '''
        print('INIT')

        request_data = {
            'command': 'INIT',
            'media_type': 'image/jpg',
            'total_bytes': self.total_bytes,
            'media_category': 'tweet_image'
        }

        req = requests.post(url=media_endpoint_url,
                            data=request_data,
                            auth=oauth)
        media_id = req.json()['media_id']

        self.media_id = media_id

        print('Media ID: %s' % str(media_id))

    def upload_append(self):
        '''
        Uploads media in chunks and appends to chunks uploaded
        '''
        segment_id = 0
        bytes_sent = 0
        file = open(self.image_filename, 'rb')

        while bytes_sent < self.total_bytes:
            chunk = file.read(4 * 1024 * 1024)

            print('APPEND')

            request_data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id
            }

            files = {
                'media': chunk
            }

            req = requests.post(url=media_endpoint_url,
                                data=request_data,
                                files=files,
                                auth=oauth)

            if req.status_code < 200 or req.status_code > 299:
                print(req.status_code)
                print(req.text)
                sys.exit(0)

            segment_id = segment_id + 1
            bytes_sent = file.tell()

            print('%s of %s bytes uploaded' % (str(bytes_sent),
                                               str(self.total_bytes)))

        print('Upload chunks complete.')

    def upload_finalize(self):
        '''
        Finalizes uploads and starts image processing
        '''
        print('FINALIZE')

        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }

        req = requests.post(url=media_endpoint_url,
                            data=request_data,
                            auth=oauth)
        print(req.json())

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()

    def check_status(self):
        '''
        Checks image processing status
        '''
        if self.processing_info is None:
            return

        state = self.processing_info['state']

        print('Media processing status is %s ' % state)

        if state == u'succeeded':
            return

        if state == u'failed':
            sys.exit(0)

        check_after_secs = self.processing_info['check_after_secs']

        print('Checking after %s seconds' % str(check_after_secs))
        time.sleep(check_after_secs)

        print('STATUS')

        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }

        req = requests.get(url=media_endpoint_url,
                           params=request_params,
                           auth=oauth)

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()

# if __name__ == '__main__':
#     imageTweet = ImageTweet(image_filename)
#     imageTweet.upload_init()
#     imageTweet.upload_append()
#     imageTweet.upload_finalize()
