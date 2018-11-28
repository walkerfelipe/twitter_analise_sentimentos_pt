# -*- encoding: utf-8 -*-
'''
Esse script tira as médias e plota graficos dos resultados anteriores
salvos no banco indicado
'''
import sqlite3
import re
import os

try:
    os.stat("images")
except:
    os.mkdir("images")       

def column(matrix, i):
    return [row[i] for row in matrix]

conn = sqlite3.connect('tweets_1.db')

c = conn.cursor()

c.execute("SELECT query FROM tweets")
rows2= c.fetchall()
rows2=column(rows2,0)
c.execute("SELECT distinct(query) FROM tweets")
rows = c.fetchall()
query=column(rows,0)
c.execute("SELECT * FROM tweets")
rows = c.fetchall()

pos_=[0]*len(query)
neg_=[0]*len(query)
subjectivy=[0]*len(query)
polarity=[0]*len(query)
polarity_pos=[0]*len(query)
count_pos=[0]*len(query)
polarity_neg=[0]*len(query)
count_neg=[0]*len(query)
#11
nltk_neg=[0]*len(query)
#12
nltk_neu=[0]*len(query)
#10
nltk_pos=[0]*len(query)
#13
nltk_compound=[0]*len(query)
for i in range(len(query)):
    z=0
    for k in range(len(rows)):
        if rows[k][4]==query[i]:
            nltk_neg[i]+=rows[k][11]
            nltk_neu[i]+=rows[k][12]
            nltk_pos[i]+=rows[k][10]
            nltk_compound[i]+=rows[k][13]
            if rows[k][6]>0:
                polarity_pos[i]+=rows[k][6]
                count_pos[i]+=1
            elif rows[k][6]<0:
                polarity_neg[i]+=rows[k][6]
                count_neg[i]+=1
            polarity[i]+=rows[k][6]
            subjectivy[i]+=rows[k][7]
            if rows[k][8]=='pos':
                pos_[i]+=1
            else:
                neg_[i]+=1
for i in range(len(query)):
    try:
        quant=rows2.count(query[i])
        if count_neg[i]!=0:
            polarity_neg[i]=polarity_neg[i]/count_neg[i]
        if count_pos[i]!=0:
            polarity_pos[i]=polarity_pos[i]/count_pos[i]
        polarity[i]=polarity[i]/quant
        subjectivy[i]=subjectivy[i]/quant
        nltk_neg[i]=nltk_neg[i]/quant
        nltk_neu[i]=nltk_neu[i]/quant
        nltk_pos[i]=nltk_pos[i]/quant
        nltk_compound[i]=nltk_compound[i]/quant
        temp=(pos_[i]*100)/(pos_[i]+neg_[i])
        neg_[i]=(neg_[i]*100)/(pos_[i]+neg_[i])
        pos_[i]=temp
    except:
        pass
arquivo = open('Medias.txt', 'w')
for i in range(len(query)):
    arquivo.write(str(query[i]))
    arquivo.write("  ==============")
    arquivo.write("\n")
    arquivo.write("nltk_neg = ")
    
    arquivo.write(str(nltk_neg[i]))
    arquivo.write("\n")
    arquivo.write("nltk_neu = ")
    
    arquivo.write(str(nltk_neu[i]))
    arquivo.write("\n")
    arquivo.write("nltk_pos = ")

    
    arquivo.write(str(nltk_compound[i]))
    arquivo.write("\n")
    arquivo.write("nltk_compound = ")
    
    arquivo.write(str(nltk_pos[i]))
    arquivo.write("\n")
    arquivo.write("subjectivy = ")

    
    arquivo.write(str(subjectivy[i]))
    arquivo.write("\n")
    arquivo.write("polarity = ")
    
    arquivo.write(str(polarity[i]))    
    arquivo.write("\n")
    arquivo.write("polarity_neg = ")
   
    arquivo.write(str(polarity_neg[i]))    
    arquivo.write("\n")
    arquivo.write("polarity_pos = ")
   
    arquivo.write(str(polarity_pos[i]))    
    arquivo.write("\n")
    arquivo.write("pos_ = ")
    
    arquivo.write(str(pos_[i]))
    arquivo.write("\n")
    arquivo.write("neg_ = ")
    
    arquivo.write(str(neg_[i]))    
    arquivo.write("\n")
    arquivo.write("\n")
arquivo.close()
############### matplot lib

import numpy as np
import matplotlib.pyplot as plt
for i in range(len(query)):
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    legendas=['pos.%','neg.%','',' média pos.','média neg.','','polarity']

    ax.bar(1,neg_[i],color="red")
    ax.text(1-0.3,neg_[i]+0.2,str(round(neg_[i],2))+" %")

    ax.bar(0,pos_[i],color="blue")
    ax.text(0-0.3,pos_[i]+0.2,str(round(pos_[i],2))+" %")


    ax.bar(3,polarity_pos[i]*100,color="blue")
    ax.text(3-0.3,polarity_pos[i]*100+0.2,str(round(100*polarity_pos[i],2))+" %")

    ax.bar(4,-1*polarity_neg[i]*100,color="red")
    ax.text(4-0.3,-1*polarity_neg[i]*100+0.2,str(round(-100*polarity_neg[i],2))+" %")

    if (polarity[i]>=0):
        ax.bar(6,abs(polarity[i])*100,color="blue")
        ax.text(6-0.3,abs(polarity[i])*100+0.2,str(round(100*polarity[i],2))+" %")
    else:
        ax.bar(6,abs(polarity[i])*100,color="red")
        ax.text(6-0.3,abs(polarity[i])*100+0.2,str(round(100*polarity[i],2))+" %")
    plt.title('TextBlob query: '+query[i])
    plt.xticks(range(len(legendas)),legendas,rotation=45)
    fig.savefig(str('./images/textblob_'+query[i]), bbox_inches='tight')
    plt.cla()   # Clear axis
    plt.clf()   # Clear figure
    plt.close() # Close a figure window
    #plt.show()
    ############### NLKT
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    legendas=['nlkt_pos%','nlkt_neg.%','nlkt_neu.%','nltk_compound']

    ax.bar(0,100*nltk_pos[i],color="blue")
    ax.text(0-0.3,100*nltk_pos[i]+0.2,str(round(100*nltk_pos[i],2))+" %")

    ax.bar(1,100*nltk_neg[i],color="red")
    ax.text(1-0.3,100*nltk_neg[i]+0.2,str(round(100*nltk_neg[i],2))+" %")

    ax.bar(2,100*nltk_neu[i],color="orange")
    ax.text(2-0.3,100*nltk_neu[i]+0.2,str(round(100*nltk_neu[i],2))+" %")

    if nltk_compound[i]>=0:
        ax.bar(3,100*abs(nltk_compound[i]),color="blue")
        ax.text(3-0.3,abs(100*nltk_compound[i])+0.2,str(round(100*nltk_compound[i],2))+" %")
    else:
        ax.bar(3,100*abs(nltk_compound[i]),color="red")
        ax.text(3-0.3,abs(100*nltk_compound[i])+0.2,str(round(100*nltk_compound[i],2))+" %")

    plt.title('NLTK query: '+query[i])
    plt.xticks(range(len(legendas)),legendas,rotation=45)
    fig.savefig(str('./images/nltk_'+query[i]), bbox_inches='tight')
    plt.cla()   # Clear axis
    plt.clf()   # Clear figure
    plt.close() # Close a figure window
