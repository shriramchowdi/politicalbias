import tweepy
import csv

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name, write_csv = False):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    except tweepy.error.TweepError:
        return False, None
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    print('collecting tweets of '+screen_name+' ........')
    while len(new_tweets) > 0:
        #print ("getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        #print ("...%s tweets downloaded so far" % (len(alltweets)))
    print ("...%s tweets collected" % (len(alltweets)))
    #transform the tweepy tweets into a 1D array that will populate the csv 
    outtweets = [tweet.text for tweet in alltweets]
    #print(outtweets[0],type(outtweets[0]))
    
    #write the csv
    if write_csv: 
        with open('%s_tweets.csv' % screen_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["text"])
            writer.writerows(outtweets)
    
    return True, outtweets


if __name__ == '__main__':
    #pass in the username of the account you want to download
    left = ['KilaFateh','usman_sagri','Swamyv39','MamataOfficial','digvijaya_28','sardesairajdeep','BDUTT','sagarikaghose','Shehla_Rashid','kanhaiyakumar','Nidhi','RanaAyyub','UmarKhalidJNU','jigneshmevani80','SitaramYechury','cpimspeak','ArvindKejriwal','divyaspandana','asadowaisi','imAkbarOwaisi','warispathan','islahmufti','VORdotcom','sanjivbhatt','ReallySwara']
    for i in left:
        get_all_tweets(i)
