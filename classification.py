#como setar variavel do google translator ( arquivo json):
#$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\username\Downloads\[FILE_NAME].json"
#necessário criar variavel antes de iniciar o python( recomendado utilizar powershell)
import sqlite3
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import os
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
nltk.download('vader_lexicon') # necessário apenas na primeira vez
sid = SentimentIntensityAnalyzer()

# Importando biblioteca de tradução do Google Cloud
from google.cloud import translate

# Instanciando o cliente, essa parte só vai funcionar
# se o arquivo json tiver sido setado na variavel GOOGLE_APPLICATION_CREDENTIALS ( no S.O ). 
try:
    translate_client = translate.Client()
except:
    pass
# necessário ser a base gerada pelo 'buscatweets.py'
conn = sqlite3.connect('tweets_1.db')
c = conn.cursor()

# Adicionando colunas para salvar o resultado das analises de sentimento
try:
    c.execute('''ALTER TABLE tweets ADD COLUMN polarity DOUBLE''')
    conn.commit()
except:
    pass

try:
    c.execute('''ALTER TABLE tweets ADD COLUMN subjectivity DOUBLE''')
    conn.commit()
except:
    pass

try:
    c.execute('''ALTER TABLE tweets ADD COLUMN pos_neg TEXT''')
    conn.commit()
except:
    pass

try:
    c.execute('''ALTER TABLE tweets ADD COLUMN text_en TEXT''')
    conn.commit()
except:
    pass
try:
    c.execute('''ALTER TABLE tweets ADD COLUMN NLTK_neg DOUBLE''')
    conn.commit()
except:
    pass

try:
    c.execute('''ALTER TABLE tweets ADD COLUMN NLTK_neu DOUBLE''')
    conn.commit()
except:
    pass

try:
    c.execute('''ALTER TABLE tweets ADD COLUMN NLTK_pos DOUBLE''')
    conn.commit()
except:
    pass

try:
    c.execute('''ALTER TABLE tweets ADD COLUMN NLTK_compound DOUBLE''')
    conn.commit()
except:
    pass

#carregando a base de dados
c.execute("SELECT * FROM tweets")
rows = c.fetchall()

'''
 Treinando o TextBlob para analisar textos em portugues.
 Essa forma, retorna apenas 'pos'(positiv) e 'neg'(negativo) para os textos analisados.
 Os arquivos foram extraidos de  ReLi (REsenha de LIvros) https://www.linguateca.pt/Repositorio/ReLi/
 
 '''
base_path = 'ReLi-Lex'
train = []
files = [os.path.join(base_path, f) for f in os.listdir(base_path)]

for file in files:
    t = 'pos' if '_Positivos' in file else 'neg'
    with open(file, 'r') as content_file:
        content = content_file.read()
        all = re.findall('\[.*?\]',content)
        for w in all:
            train.append((w[1:-1], t))

cl = NaiveBayesClassifier(train)

#Analise com TextBlob em pt ( utilizando treinamento )
print("Processando Polarity 'pos' ou 'neg':")
for i in range(len(rows)):
    print(str(i)+" de "+str(len(rows)) )
    blob=TextBlob(rows[i][2],classifier=cl)
    resp=blob.classify()
    c.execute("UPDATE tweets SET pos_neg='"+resp+"' WHERE id='"+rows[i][5]+"' ")
    conn.commit()

    # traduzindo para 'en' e aplicando a analise do textblob( nativa em ingles)
print("Processando subjectivity e polarity:")
for i in range(len(rows)):
    print(str(i)+" de "+str(len(rows)) )
    # Forma antiga, onde usa tradutor do proprio blob ( é limitado ... )
    
    try:
        texto_en=translate_client.translate(rows[i][2],target_language='en')
        blob=TextBlob(texto_en['translatedText'])
    except:
        blob=TextBlob(rows[i][2])
        blob=blob.translate(to="en")
 
    # caso utilize a API do google cloud, comente as 2 linhas acima, e descomente as 2 abaixo

    ####
    c.execute("UPDATE tweets SET subjectivity='"+str(blob.sentiment.subjectivity)+"',polarity='"+str(blob.sentiment.polarity)+"' WHERE id='"+rows[i][5]+"' ")
    c.execute("UPDATE tweets SET text_en ='"+str(blob).replace("'","")+"' WHERE id='"+rows[i][5]+"' ")
    conn.commit()    

c.execute("SELECT * FROM tweets")
rows = c.fetchall()

# Analisando Com NLTK, tambem em ingles. Textos traduzidos anteriormente já foram salvos
print("Processing NLTK:")
for i in range(len(rows)):
    print(str(i)+" de "+str(len(rows)) )
    text_en=str(rows[i][9])
    ss=sid.polarity_scores(text_en)
    c.execute("UPDATE tweets SET NLTK_neg='"+str(ss['neg'])+"',NLTK_neu='"+str(ss['neu'])+"', NLTK_pos='"+str(ss['pos'])+"',NLTK_compound='"+str(ss['compound'])+"' WHERE id='"+rows[i][5]+"' ")
    conn.commit() 

conn.close()