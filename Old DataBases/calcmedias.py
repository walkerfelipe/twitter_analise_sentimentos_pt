# -*- encoding: utf-8 -*-
import sqlite3
import re
import os
def column(matrix, i):
    return [row[i] for row in matrix]

#conn = sqlite3.connect('base2001.db')
conn = sqlite3.connect('tweets_combinados_30_10_2018.db')
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
    quant=rows2.count(query[i])
    #quant_pos=sum(n > 0 for n in column(rows,6))
    #quant_neg=sum(n < 0 for n in column(rows,6))
    polarity_neg[i]=polarity_neg[i]/count_neg[i]
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