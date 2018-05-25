import http.client
import json
import urllib

from parse_credentials import *


# Object for each post
class Post(object):
    def __init__(self,
                 title='',
                 description='',
                 media=[],
                 day='',
                 month='',
                 year='',
                 identification=''):
        self.title = title
        self.description = description
        self.media = media
        self.day = day
        self.month = month
        self.year = year
        self.identification = identification

    def add_title(self, title):
        self.title = title

    def add_description(self, description):
        self.description = description

    def add_media(self, media):
        self.media.append(media)

    def add_day(self, day):
        self.day = day

    def add_month(self, month):
        self.month = month

    def add_year(self, year):
        self.year = year

    def add_identification(self, identification):
        self.identification = identification

    def get_title(self):
        print(self.title)

    def get_description(self):
        print(self.description)

    def get_media(self):
        print(self.media)

    def get_day(self):
        print(self.day)

    def get_month(self):
        print(self.month)

    def get_year(self):
        print(self.year)

    def identification(self):
        print(self.identification)

    def __str__(self):
        print(self.day)
        print(self.month)
        print(self.year)
        print(self.title)
        print(self.description)
        print(self.media)
        print(self.identification)
        return ''


# Function for calling all relevant posts for a particular date
def get_posts(month, day):
    # Establish connection
    connection = http.client.HTTPSConnection(server_url, 443)
    # Filter for specific date
    params = urllib.urlencode({"where": json.dumps({
        "month": month,
        "day": day
    })})
    connection.connect()
    connection.request('GET', '/parse/classes/<YOUR_CLASS_NAME>?%s' % params, '', {
        "X-Parse-Application-Id": app_id,
        "X-Parse-REST-API-Key": client_key
    })
    response = json.loads(connection.getresponse().read())

    # Make list of all relevant post objects
    posts = []
    for post in response['results']:
        post['objectId'] = Post(post['title'].encode('utf-8'),
                                post['description'].encode('utf-8'),
                                post['media'],
                                post['day'],
                                post['month'],
                                post['year'],
                                post['objectId'])
        posts.append(post['objectId'])

    return posts
