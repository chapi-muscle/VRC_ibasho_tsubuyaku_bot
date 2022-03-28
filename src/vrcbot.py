import requests
import os
from dotenv import load_dotenv
import time
import json
import datetime
import tweepy

# authentification
load_dotenv()
# vrchat
base_url = 'http://api.vrchat.cloud/api/1'
username = os.environ['USER_ID']
password = os.environ['PASSWORD']
api_key = 'JlE5Jldo5Jibnk5O5hTx6XVqsJu4WJ26' # common to everyone
data = {'apiKey':api_key}
headers = {'User-Agent': 'chapichapi'}
r = requests.get(f'{base_url}/auth/user', headers=headers, auth=(username, password))
auth_token = r.cookies['auth']

# twitter
consumer_key = os.getenv('API_KEY')
consumer_secret = os.getenv('API_SECRET_KEY')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_SECRET_TOKEN')
client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)


time.sleep(90)


world_id_prev = '0'
while(True):
    try:
        r = requests.get(f'{base_url}/auth/user/friends', headers=headers, params={'apiKey':api_key, 'authToken': auth_token})
    except requests.exceptions.HTTPError as e:
        print(f'Error occur : {e}')
        time.sleep(90)
        continue
    
    if (len(json.loads(r.content)) < 1):
        time.sleep(90)
        continue
    
    if (json.loads(r.content)[0]['location'] and json.loads(r.content)[0]['location'].split(':')[0] != 'private'):
        world_id = json.loads(r.content)[0]['location'].split(':')[0]
    else:
        time.sleep(90)
        continue
    
    if (world_id != world_id_prev):
        world_id_prev = world_id
        time.sleep(90)
        print(datetime.datetime.today()+datetime.timedelta(seconds=32400))
        try:
            r = requests.get(f'{base_url}/worlds/{world_id}', headers=headers, params={'apiKey':api_key, 'authToken': auth_token})
        except requests.exceptions.HTTPError as e:
            print(f'Error occur : {e}')
            time.sleep(90)
            continue
        
        whereiam = json.loads(r.content)['name']
        try:
            client.create_tweet(text=f'I am in {whereiam}')
        except tweepy.errors.TweepyException as e:
            print(e)
    
    time.sleep(90)