# -*- encoding: utf-8 -*-
import tweepy
import sqlite3
'''
Esse script busca os tweets e salva em banco de dados local
utilizando sqlite3
'''
#Palavras buscadas 
#query =['ditadura','facismo','Brasil,medo','eleições,medo','facismo,brasil','ditadura,medo','medo,bolsonaro','eleições,bolsonaro','voto,eleições','voto,bolsonaro','bolsonaro,desenvolvimento','haddad,ladrão','lula,ladrão','haddad,socialismo','fake news','whatsapp,espalhar','espalhar,fake news','governo,povo','mourão,militar','manuela d\'ávila','stf','mourão']

query=['stan lee','marvel']
# numero maximo de tweets para cada palavra( para o trabalho buscamos 2000)
max_tweets = 10

#Conexão com banco de dados 
conn = sqlite3.connect('tweets_1.db')
c = conn.cursor()
#criando tabelas se não existirem
c.execute('''Create TABLE if not exists tweets("display_name","name","text","data","query",id PRIMARY KEY)''')

#função de inserir no banco
def data_entry():
    for i in range(len(tweets_encontrados)):
        try:
            if 'retweeted_status' in dir(tweets_encontrados[i]):
                c.execute("INSERT INTO tweets('name','display_name','text','data','query','id') VALUES('"+tweets_encontrados[i].user.screen_name.replace("'","")+"','"+tweets_encontrados[i].user.name.replace("'","")+"','"+tweets_encontrados[i].retweeted_status.full_text.replace("'","")+"','"+str(tweets_encontrados[i].created_at)+"','"+query[n]+"','"+str(tweets_encontrados[i].id)+"')")
            else:
                c.execute("INSERT INTO tweets('name','display_name','text','data','query','id') VALUES('"+tweets_encontrados[i].user.screen_name.replace("'","")+"','"+tweets_encontrados[i].user.name.replace("'","")+"','"+tweets_encontrados[i].full_text.replace("'","")+"','"+str(tweets_encontrados[i].created_at)+"','"+query[n]+"','"+str(tweets_encontrados[i].id)+"')")
            conn.commit()
        except:
            pass

#Autenticação do Twitter
auth = tweepy.OAuthHandler("gfU74Yf0e52dR7QTjhqlmHiEO", "yRSpI5dTZVs0AMocMwUwO5cw0vhNsazS7YtQzTk8Wob8t3RB4b")
auth.set_access_token("2170605474-XyPs0zpvCrl27d11TWGDhbEAklotElJc48Y3bhP", "5pHPIkKF2KreBB2ZyBpfs2WMBgCVHMCsv2fDtQXPu9CZ9")
api = tweepy.API(auth)
#parte de busca dos tweets
for n in range(len(query)):
    print("Buscando por "+query[n]+" -- "+str(n+1)+" de "+str(len(query)))
    count=0
    tweets_encontrados = []
    last_id = -1
    while len(tweets_encontrados) < max_tweets:
        
        count = max_tweets - len(tweets_encontrados)
        try: #until='2018-11-02' # parametro, buscar antes dessa data ( max ~ 1 semana)
            new_tweets = api.search(q=query[n],lang = 'pt' ,count=count,tweet_mode='extended',max_id=str(last_id - 1))
            if not new_tweets:
                break
            tweets_encontrados.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Desistir caso haja algum erro
            break
    data_entry()
    del tweets_encontrados
conn.close() # close conexão com banco de dados
