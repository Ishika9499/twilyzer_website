import matplotlib.pyplot as plt
from matplotlib import style
def donutchart(sentiment1):
    # Donut Chart

    sentiment = sentiment1
    ptweet = [tweet['sentiment'] for tweet in sentiment if tweet['sentiment'] == 'Positive']
    ntweet = [tweet['sentiment'] for tweet in sentiment if tweet['sentiment'] == 'Negative']
    neutweet = [tweet['sentiment'] for tweet in sentiment if tweet['sentiment'] == 'Neutral']
    per_ptweets = (100 * len(ptweet)) / len(sentiment)
    per_ntweets = (100 * len(ntweet)) / len(sentiment)
    per_neutweets = (100 * len(neutweet)) / len(sentiment)
    # print(per_ptweets)
    # print(per_ntweets)

    names = ['Positive', 'Negative', 'Neutral']
    percentage = [per_ptweets, per_ntweets, per_neutweets]
    f2 = plt.figure()
    f2.set_figwidth(10)
    f2.set_figheight(10)
    my_circle = plt.Circle((0, 0), 0.7, color='white')

    # Give color names
    
    plt.pie(percentage, labels=names, autopct='%1.1f%%',
            colors=['green', 'red', 'grey'])

    p = plt.gcf()
    p.gca().add_artist(my_circle)

    # Saving the Graph
    plt.savefig('static/images/figure2.png')
    plt.clf()