import json
import tweepy
import random
import time


def connexion(tokens):
    consumer_key = tokens["5G3GOAfVc9ZNP3W83lPUkvIVv"]
    consumer_secret = tokens["9oowgDbMlHUR5mZlqbu5nj9VhzGk355dJqlkOPu5ET8dz3FRjq"]
    access_token = tokens["1271688482793160705-2rGfv6a2WFd8bYZ8DDQW1PjW8lRlDi"]
    access_token_secret = tokens["Vq31qs4gq9cMXsd07YrsK3d75PZECPKqpKorpwkgzQOCy"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return auth, api


def load_config():
    """
    return the data from config.json
    """
    # load the tokens and the account to follow
    data = {"5G3GOAfVc9ZNP3W83lPUkvIVv": "", "9oowgDbMlHUR5mZlqbu5nj9VhzGk355dJqlkOPu5ET8dz3FRjq": "",
            "1271688482793160705-2rGfv6a2WFd8bYZ8DDQW1PjW8lRlDi": "", "Vq31qs4gq9cMXsd07YrsK3d75PZECPKqpKorpwkgzQOCy": ""}
    try:
        with open("config.json", "r") as f:
            data = json.load(f)
            return data
    except:
        # if the file don't exist create a new one
        with open("config.json", "w") as f:
            json.dump(data, f)
            return data


config = load_config()
auth, api = connexion(config)


try:
    api.me()
    # Check if the tokens are good
    print("succefuly connected to {}".format(api.me().screen_name))
    ok = True
except:
    print("Not connected \nplease fill the config file with your tokens")
    ok = False


def retweet_for_hashtag(hashtag):
    raw_tweets = tweepy.Cursor(
        api.search, q=hashtag, lang="en", result_type="latest").items(10)
    try:
        for tweet in raw_tweets:
            print(tweet.text)
            if tweet.text[:2] != "RT" and tweet.text[:1] != "@":
                api.retweet(tweet.id)
                print("retweeted")
                return
    except Exception as e:
        time.sleep(60)


if ok:
    while True:
        with open("hashtags.txt") as f:
            a = f.readlines()
        for hashtag in a:
            try:
                print(hashtag)
                hashtag = hashtag.replace("\n", "")
                print(hashtag)
                retweet_for_hashtag(hashtag)
                time.sleep(80)
            except :
                pass
