import matplotlib.pyplot as plt
from matplotlib import style
import text2emotion as te
def bargraph(process_tweet):
    tweets = process_tweet
    emotion = []
    sum_happy = 0
    sum_angry = 0
    sum_surprise = 0
    sum_sad = 0
    sum_fear = 0
    for tweet in tweets:
        emo = te.get_emotion(tweet['text'])
        sum_happy = sum_happy + emo['Happy']
        sum_angry = sum_angry + emo['Angry']
        sum_surprise = sum_surprise + emo['Surprise']
        sum_sad = sum_sad + emo['Sad']
        sum_fear = sum_fear + emo['Fear']
    avg_happy = sum_happy / len(tweets)
    avg_angry = sum_angry / len(tweets)
    avg_surprise = sum_surprise / len(tweets)
    avg_sad = sum_sad / len(tweets)
    avg_fear = sum_fear / len(tweets)
    y = ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']

    # getting values against each value of y
    x = [avg_happy * 100, avg_angry * 100, avg_surprise * 100, avg_sad * 100, avg_fear * 100]
    colour = ['Yellow', 'Red', 'Blue', 'Grey', 'Purple']
    f3 = plt.figure()
    f3.set_figwidth(12)
    f3.set_figheight(8)
    plt.barh(y, x, color = colour)

    # setting label of y-axis
    plt.ylabel("Emotions", fontsize=14)

    # setting label of x-axis
    plt.xlabel("Average Polarity(%)", fontsize=14)
    plt.title("Horizontal bar graph", fontsize=14)
    # print(len(tweets))
    plt.savefig('static/images/figure3.png')
    plt.clf()