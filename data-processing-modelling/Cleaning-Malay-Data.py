
import json
import malaya
import pandas as pd
import matplotlib.pyplot as plt
import re
import csv
import nltk
from nltk.corpus import stopwords
import numpy as np, pylab as pl
from sklearn import metrics
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer


cols = ['text']
path = 'data/'
file = 'malayonly[RAW]'
filename = path+file+'.csv'
lang = 'malay'
df = 'df'+lang

df = pd.read_csv(filename)

#df.head()
df.count()


# In[27]:


df.head(7)


# # REMOVE DUPLICATE

# In[28]:


checkdup=[]

for line in df['text']:
    line = line.lower()
    if line not in checkdup:
        checkdup.append(line)
    
df = pd.DataFrame({'text':checkdup})
#df.head()
df.count()

print("Done!!")


# In[29]:


df.count()


# # REMOVE RETWEET & SWARMP

# In[30]:


df = df[df.text.str.contains("rt") == False] #remove RT
df=df[df.text.str.contains("I'm") == False]
df = df[df.text.str.contains("gwa") == False]
df = df[df.text.str.contains("sih") == False]

df.count()

print("Done!!")


# In[31]:


df.count()


# # REMOVE PUNTUATION

# In[32]:


remlink = []

for i in df['text']:
    a = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",i)
    remlink.append(a)
    
df['text'] = remlink 

print("Done!!")


# In[33]:


df.count()


# # REMOVE STOPWORD

# In[34]:


stop = stopwords.words("english") #FOR ENGLISH
stop_words = set({'ada','inikah','sampai','adakah','inilah','sana','adakah','itu','sangat','adalah','itukah','sangatlah','adanya','itulah','saya','adapun','jadi','se','agak','jangan','seandainya','agar','janganlah','sebab','akan','jika','sebagai','aku','jikalau','sebagaimana','akulah','jua','sebanyak','akupun','juapun','sebelum','al','juga','sebelummu','alangkah','kalau','sebelumnya','allah','kami','sebenarnya','amat','kamikah','secara','antara','kamipun','sedang','antaramu','kamu','sedangkan','antaranya','kamukah','sedikit','apa','kamupun','sedikitpun','apa-apa','katakan','segala','apabila','ke','sehingga','apakah','kecuali','sejak','apapun','kelak','sekalian','atas','kembali','sekalipun','atasmu','kemudian','sekarang','atasnya','kepada','sekitar','atau','kepadaku','selain','ataukah','kepadakulah','selalu','ataupun','kepadamu','selama','bagaimana','kepadanya','selama-lamanya','bagaimanakah','kepadanyalah','seluruh','bagi','kerana','seluruhnya','bagimu','kerananya','sementara','baginya','kesan','semua','bahawa','ketika','semuanya','bahawasanya','kini','semula','bahkan','kita','senantiasa','bahwa','ku','sendiri','banyak','kurang','sentiasa','banyaknya','lagi','seolah','barangsiapa','lain','seolah-olah','bawah','lalu','seorangpun','beberapa','lamanya','separuh','begitu','langsung','sepatutnya','begitupun','lebih','seperti','belaka','maha','seraya','belum','mahu','sering','belumkah','mahukah','serta','berada','mahupun','seseorang','berapa','maka','sesiapa','berikan','malah','sesuatu','beriman','mana','sesudah','berkenaan','manakah','sesudahnya','berupa','manapun','sesungguhnya','beserta','masih','sesungguhnyakah','biarpun','masing','setelah','bila','masing-masing','setiap','bilakah','melainkan','siapa','bilamana','memang','siapakah','bisa','mempunyai','sini','boleh','mendapat','situ','bukan','mendapati','situlah','bukankah','mendapatkan','suatu','bukanlah','mengadakan','sudah','dahulu','mengapa','sudahkah','dalam','mengapakah','sungguh','dalamnya','mengenai','sungguhpun','dan','menjadi','supaya','dapat','menyebabkan','tadinya','dapati','menyebabkannya','tahukah','dapatkah','mereka','tak','dapatlah','merekalah','tanpa','dari','merekapun','tanya','daripada','meskipun','tanyakanlah','daripadaku','mu','tapi','daripadamu','nescaya','telah','daripadanya','niscaya','tentang','demi','nya','tentu','demikian','olah','terdapat','demikianlah','oleh','terhadap','dengan','orang','terhadapmu','dengannya','pada','termasuk','di','padahal','terpaksa','dia','padamu','tertentu','dialah','padanya','tetapi','didapat','paling','tiada','didapati','para','tiadakah','dimanakah','pasti','tiadalah','engkau','patut','tiap','engkaukah','patutkah','tiap-tiap','engkaulah','per','tidak','engkaupun','pergilah','tidakkah','hai','perkara','tidaklah','hampir','perkaranya','turut','hampir-hampir','perlu','untuk','hanya','pernah','untukmu','hanyalah','pertama','wahai','hendak','pula','walau','hendaklah','pun','walaupun','hingga','sahaja','ya','ia','saja','yaini','iaitu','saling','yaitu','ialah','sama','yakni','ianya','yang','inginkah','samakah','ini','sambil'})

df['text'] = df['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))

df.count()

print("Done!!")


# In[35]:


df.head(8)


# # NUMBER TO TEXT

# In[36]:


count=0
clean=[]
ab=[]

for i,row in df.iterrows():
    s = row['text'].split()
    
    for item in s:
        if item.isdigit() == True:
            item=malaya.to_cardinal(int(item))  
        clean.append(item)
    count+=1
    a=' '.join(clean)
    ab.append(a)
    clean=[]
    
df['text-after-1st-proc']=ab

print("Done!!")


# In[37]:


df.head(8)


# # NORMALIZE

# In[38]:


clean=[]
abc=[]
count=df['text-after-1st-proc'].count()
malays = malaya.load_malay_dictionary()
normalizer = malaya.fuzzy_normalizer(malays)    

for item in df["text-after-1st-proc"]: #hjhjjhh
    item=normalizer.normalize(item)
    count-=1
    print("{}) {}".format(count,item))
    clean.append(item)
    
df['text-after-norm']=clean

print("Done!!")


# In[ ]:


df.head(7)


# # SPELLING CORRECTOR

# In[ ]:


clean=[]
abc=[]
count1=df['text-after-norm'].count()
malays = malaya.load_malay_dictionary()
corrector = malaya.naive_speller(malays)    

for i,row in df.iterrows():
    count1-=1
    s = row['text-after-norm'].split()
    for item in s :
        if len(item)>1:
            item=corrector.correct(item)
        clean.append(item)

    a=' '.join(clean)
    print("\n|| (AFTER) ---> {}\n".format(a))
    abc.append(a)
    clean=[]
    print("(REMAINING) : {}\n\n".format(count1))
df['text-after-spell']=abc

print("Done!!")


# In[ ]:


df.head()


# # STEMMING

# In[ ]:


clean=[]
ab=[]
stemmer = malaya.deep_stemmer()
count1=df['text-after-spell'].count()
dfnew=[]
print(count1)

for i in df['text-after-spell']:
    count1-=1
    a=malaya.sastrawi_stemmer(i)
    print("{}) {}".format(count1,a))
    ab.append(a)
    
#print(count)    
df['text-after-stemming'] = ab


# In[ ]:


df.head()


# In[ ]:


df.to_csv("DONE-PROCESS-DATA-7K-LATES 28 NOV.csv", encoding='utf-8',header=True, index=False)

