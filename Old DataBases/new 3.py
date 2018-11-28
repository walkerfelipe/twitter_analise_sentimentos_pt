# -*- encoding: utf-8 -*-
#https://medium.com/@viniljf/criando-um-analisador-de-sentimentos-para-tweets-a53bae0c5147
import tweepy
import sqlite3

################ Banco de dados 
conn = sqlite3.connect('tweets_teste.db')
c = conn.cursor()

#Create table
c.execute('''Create TABLE if not exists tweets("display_name","name","text","data","query",id PRIMARY KEY)''')

def data_entry():
	#i=0
	for i in range(len(searched_tweets)):
		if 'retweeted_status' in dir(searched_tweets[i]):
			c.execute("INSERT INTO tweets('name','display_name','text','data','query','id') VALUES('"+searched_tweets[i].user.screen_name.replace("'","")+"','"+searched_tweets[i].user.name.replace("'","")+"','"+searched_tweets[i].retweeted_status.full_text.replace("'","")+"','"+str(searched_tweets[i].created_at)+"','"+query+"','"+str(searched_tweets[i].id)+"')")
		else:
			c.execute("INSERT INTO tweets('name','display_name','text','data','query','id') VALUES('"+searched_tweets[i].user.screen_name.replace("'","")+"','"+searched_tweets[i].user.name.replace("'","")+"','"+searched_tweets[i].full_text.replace("'","")+"','"+str(searched_tweets[i].created_at)+"','"+query+"','"+str(searched_tweets[i].id)+"')")
	#c.execute("INSERT INTO tweets('name','text','data') VALUES('{0}','{1}','teste')".format(list_[i],list2_[i]) )
	conn.commit()

################

# assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)
#from twitter_authentication import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler("gfU74Yf0e52dR7QTjhqlmHiEO", "yRSpI5dTZVs0AMocMwUwO5cw0vhNsazS7YtQzTk8Wob8t3RB4b")
auth.set_access_token("2170605474-XyPs0zpvCrl27d11TWGDhbEAklotElJc48Y3bhP", "5pHPIkKF2KreBB2ZyBpfs2WMBgCVHMCsv2fDtQXPu9CZ9")

api = tweepy.API(auth)

#66
query = 'mourão'
max_tweets = 5
#searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
searched_tweets = []
last_id = -1
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query,lang = 'pt', count=count,tweet_mode='extended',max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break
data_entry()
conn.close()


##SALVANDO EM ARQUIVO 
#print (searched_tweets)
#file = open("testfile.txt","w") 
#file.write(str(searched_tweets)) 
#file.close() 
#print ("TEXTO DO TWITTER: "+str(searched_tweets[0].text))

## ALGUNS PRINTS ###
#searched_tweets[0].created_at # data e hora do tweet 
#searched_tweets[0].text # texto do twitter 
#searched_tweets[0].user.screen_name # nome do usuario 
#searched_tweets[0].user.name # nome @algumacoisa

# imprimir texto grande 
#searched_tweets[0].retweeted_status.full_text

#SALVAMENTO QUE FUNCIONA. 
#	with open("teste2.txt" , "w", encoding="utf-8") as f:
#		f.write(str(searched_tweets[1]._json))

# Descobrindo se é um retweet
#i=0
#for i in range(10):
#   print(searched_tweets[i].full_text)
#for i in range(11):
#    print(i)
#if 'retweeted_status' in dir(searched_tweets[1]):
#   print ("é um retwit")
#else:
#   print (" não é ")