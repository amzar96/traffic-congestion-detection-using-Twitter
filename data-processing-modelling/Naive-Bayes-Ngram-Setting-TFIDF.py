import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import pickle
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.preprocessing import normalize
pd.set_option('display.notebook_repr_html', True)


''' Load Data & Prepare''' 
'''___________________________'''
path = 'data/malay5k.csv'
tweets = pd.read_csv(path)
display(tweets.head(2))

tweets['label_num'] = tweets.label.map({'no':0, 'yes':1})

X = tweets.text_after_stemming
y = tweets.label_num
'''___________________________'''



''' Prepare for Classification''' 
'''___________________________'''
size=0.15
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size, random_state=1)

#TfidfVectorizer is a combination of Countvectorizer + TF-IDF
ngram_range = (str("1,3"))
vectorizer = TfidfVectorizer(ngram_range=(1,3))
vectorizer.fit(X)

X_train_dtm = vectorizer.fit_transform(X_train)

#print(X_train_dtm)

#Feature Name
print("Features Name\n")
#display(vectorizer.get_feature_names())
#display(vectorizer.vocabulary_)

feature_names = vectorizer.get_feature_names()
#print(len(feature_names))
#display(feature_names[50:70])
#print(X_train_dtm.)
dense = X_train_dtm.todense()
episode = dense[0].tolist()[0]
phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]
sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores][:20]:
    print('{0: <20} {1}'.format(phrase, score))

clf = MultinomialNB()

y_train=y_train.astype('int')
clf=clf.fit(X_train_dtm, y_train)

X_new = vectorizer.transform(X_test)
predicted = clf.predict(X_new)

accuracy          = metrics.accuracy_score(y_test, predicted)
confusion_matrix  = metrics.confusion_matrix(y_test, predicted)
report            = classification_report(y_test, predicted)

print("\n Setting")
print("\n Vectorize : TfidfVectorizer \n Test Size : {} \n Ngram     : {}".format(size, ngram_range))
print("\n____________________________")
print("Accuracy: {}\n".format(str(round(accuracy,5))))
print("\n____________________________")
print("Confusion Matrix:\n {}\n".format(str(confusion_matrix)))
print("\n____________________________")
print("Classification Details:\n {}".format(str(report)))
