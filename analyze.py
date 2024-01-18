from flask import Flask, render_template, request, redirect
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt3
import _thread
from donut import donutchart
from bar import bargraph
import datetime
from config import *
import re
import tweepy
import nltk
import text2emotion as te
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from matplotlib import style
from datetime import *
from tweepy import OAuthHandler
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from wordcloud import WordCloud

ps = PorterStemmer()
wnet = WordNetLemmatizer()
sentintensity = SentimentIntensityAnalyzer()

all_stopwords = stopwords.words('english')
all_stopwords.remove('not')


class SentimentAnalysisNLTK:
    def clean_tweets(self, i):
        review = re.sub('[^a-zA-Z]', ' ', i)
        review = re.sub('@[A-Za-z0-9_]', ' ', review)
        review = re.sub('#[A-Za-z0-9_]', ' ', review)
        review = re.sub(r'http\S+', ' ', review)
        review = review.lower()
        review = review.split()
        # review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
        review = [wnet.lemmatize(word) for word in review if not word in set(all_stopwords)]
        review = ' '.join(review)
        return review

    def getAPI(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'cCeLYavgdGxAshXgdjnnOP00d'
        consumer_secret = '5huL70jhp9XDofoa2caS4qkeFBX7nVm21JDJ2a4u5z6WZE3a26'
        access_token = '4266630372-rrf7ukYXdfLHxQFHk8HOZfiXICpAf71NYPDpWoD'
        access_token_secret = 'NZGKLBLcx34S0QUMqUk4RzfYPboeW09yZPTE9PwH0kWYs'
        bearer_token = 'AAAAAAAAAAAAAAAAAAAAAFOycQEAAAAA%2B%2B3OopBtERwbG2Yu1f%2F3vNShYlI%3DTLshPv6ciYxXhALCRx3nMkR3SA1R8q3UrYycxSe8Kif7hQwDSt'
        # attempt authentication
        try:
            # create OAuthHandler object
            auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            api = tweepy.API(auth)
            return api

        except:
            print("Error: Authentication Failed")

    def fetch_tweets(self, keyword):
        obj1 = SentimentAnalysisNLTK()
        # Main function to fetch tweets and parse them
        # query = input("Enter the query = ")
        # count = int(input("Enter the count = "))
        query = keyword
        tweets_fetched = []
        # empty list to store parsed tweets
        try:
            # call Twitter api to fetch tweets
            api = self.getAPI()
            for i in range(0, 9):
                tweets = api.search_tweets(q=query, count=100, lang='en', until=date.today() - timedelta(i))
                if not tweets is None and len(tweets) > 0:
                    for tweet in tweets:
                        parsed_tweet = {}
                        # saving text of tweet
                        parsed_tweet['text'] = tweet.text
                        parsed_tweet['id'] = tweet.id
                        parsed_tweet['created at'] = tweet.created_at
                        # saving sentiment of tweet
                        tweets_fetched.append(parsed_tweet)
            # print(tweets_fetched)
            obj1.process_tweet(tweets_fetched)
            wordcloud(tweets_fetched)

        except Exception as e:
            print("Error : " + str(e))

    def process_tweet(self, tweet1):
        tweets_processed = []
        try:
            tweets = tweet1
            if not tweets is None and len(tweets) > 0:
                for tweet in tweets:
                    parsed_tweet = {}
                    # saving text of tweet
                    parsed_tweet['text'] = tweet['text']
                    parsed_tweet['id'] = tweet['id']
                    parsed_tweet['created at'] = tweet['created at']
                    # saving sentiment of tweet
                    tweets_processed.append(parsed_tweet)

            bargraph(tweets_processed)
            obj.tweet_sentiment(tweets_processed)
            

        except Exception as e:
            print("Error : " + str(e))


    def tweet_sentiment(self, tweet1):
        sentiment = []
        try:
            tweets = tweet1
            for tweet in tweets:
                dict = {}
                dict['id'] = tweet['id']
                dict['created at'] = tweet['created at']
                sent = sentintensity.polarity_scores(tweet['text'])['compound']
                if sent > 0:
                    dict['sentiment'] = 'Positive'
                elif sent < 0:
                    dict['sentiment'] = 'Negative'
                elif sent == 0:
                    dict['sentiment'] = 'Neutral'
                sentiment.append(dict)

            linechart(sentiment)
            donutchart(sentiment)
        except Exception as e:
            print("Error : "+str(e))    


obj = SentimentAnalysisNLTK()


def linechart(sentiment1):
    # Line Chart
    sentiment = sentiment1
    # for tweet in sentiment:
    #    print(datetime.date(tweet['created at']))
    final = []
    for i in range(1, 9):
        tweets = []
        ptweets = [tweet['sentiment'] for tweet in sentiment if tweet['sentiment'] == 'Positive' and datetime.date(tweet['created at']) ==
                   date.today() + timedelta(i - 9)]
        ntweets = [tweet['sentiment'] for tweet in sentiment if tweet['sentiment'] == 'Negative' and datetime.date(tweet['created at']) ==
                   date.today() + timedelta(i - 9)]
        netweets = [tweet['sentiment'] for tweet in sentiment if tweet['sentiment'] == 'Neutral' and datetime.date(tweet['created at']) ==
                    date.today() + timedelta(i - 9)]
        tweets.append(date.today() + timedelta(i - 9))
        tweets.append(len(ptweets))
        tweets.append(len(ntweets))
        tweets.append(len(netweets))
        final.append(tweets)
    print(final)
    x = [tweet[0] for tweet in final]
    y1 = [tweet[1] for tweet in final]
    y2 = [tweet[2] for tweet in final]
    y3 = [tweet[3] for tweet in final]
    f = plt.figure()
    f.set_figwidth(12)
    f.set_figheight(9)
    plt.plot(x, y1, color='green', label="Positive Tweets")
    plt.plot(x, y2, color='red', label="Negative Tweets")
    plt.plot(x, y3, color='yellow', label="Neutral Tweets")
    plt.legend()
    plt.savefig('static/images/figure1.png')
    plt.clf()


def wordcloud(tweet):
    tweets = tweet
    all_words = " ".join([sentence['text'] for sentence in tweets])
    wordcloud = WordCloud(width=1920, height=1080, random_state=50, max_font_size=100).generate(all_words)
    f = plt.figure()
    f.set_figwidth(20)
    f.set_figheight(12)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('static/images/figure5.png')
    plt.clf()



