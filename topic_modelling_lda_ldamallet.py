# -*- coding: utf-8 -*-
"""Topic_Modelling_LDA_LDAMallet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PAH_amajDLq3rdvkuDVfG97V0moCziQt

**Topic Modelling (Using LDA and LDAMallet) : Unsupervised**

Topic modeling is an unsupervised machine learning algorithm used for efficient processing of large collections of data, inturn applied for classification, clustering or summarization tasks. In this project LDA and LDAMallet have been used for topic extraction. LDA is a generative probabilistic model, specifically a three-level hierarchical Bayesian model, used for a collection of discrete data (such as a text corpora). Dirichlet distributions allow for probability distribution sampling over a probability simplex in which all the numbers add up to 1, and these numbers represent probabilities over K distinct categories. LDAMallet is a sampling based implementation of LDA.
"""

#Mounting gdrive to gain access to the dataset
from google.colab import drive
drive.mount("/content/gdrive")

!pip install pyLDAvis

"""**Libraries** - Gensim is used for modelling of LDA algorithm as it also provides the wrapper for LDAMallet and hence implementation of both can be done and performances can be compared. Other libraries are used for data preprocessing, visualization, etc."""

# Commented out IPython magic to ensure Python compatibility.
#Importing necessary libraries
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim_models
from nltk.stem import WordNetLemmatizer, SnowballStemmer
import numpy as np
import nltk
nltk.download('wordnet')
import pandas as pd
import json
import matplotlib.pyplot as plt
# %matplotlib inline

"""**Data** - The dataset used for this implementation is the cranfield dataset. It contains 1400 abstracts of aerodynamics journal articles from the
collection of academic papers of the college and is available for public use.
"""

#importing data
data = pd.read_json('/content/gdrive/My Drive/cran_d.json')
data

data.drop(['author', 'bibliography','title'], axis = 1)

"""**Data Preprocessing:**  - The preprocessing steps invlove cleaning the text data off the stopwords, punctuation, tokenized, lemmatized and stemmed"""

#Data Preprocessing
stemmer = SnowballStemmer(language='english')
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

processed_data = data['body'].map(preprocess)
processed_data

"""**Creation of Dictionary and the corpus for the LDA model**"""

#Creating dictionary and the word corpus
dictionary = corpora.Dictionary(processed_data)
corpus = [dictionary.doc2bow(text) for text in processed_data]

corpus_1399 = corpus[1399]
for i in range(len(corpus_1399)):
    print("Word {} (\"{}\") appears {} time.".format(corpus_1399[i][0], 
                                               dictionary[corpus_1399[i][0]], 
                                               corpus_1399[i][1]))

import pickle
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dict.gensim')

"""**Model Building and displaying the topics identified by the model** """

#with number of topics chosen randomly as 10 and the number of passes 10
NUM_TOPICS = 10
ldam10p10 = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=10)
ldam10p10.save('model10pass10.gensim')
topics = ldam10p10.print_topics(num_words=4)
for topic in topics:
    print(topic)

#with number of topics chosen randomly as 10 and the number of passes 15
NUM_TOPICS = 10
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model10pass15.gensim')
topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)

"""**Performance Evaluation of the Model**

Perplexity is the measure of how well a model predicts a sample. A lower perplexity indicates that the data is more likely. When the number of topics increase, the perplexity of the model will decrease.The coherence score assesses the quality of the learned topics. The higher the coherence score the better the model performance is.
"""

#Computing Perplexity
print('\nPerplexity: ', ldamodel.log_perplexity(corpus))

#Computing Coherence Score
coherence_ldamodel = CoherenceModel(model=ldamodel, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_lda = coherence_ldamodel.get_coherence()
print('\nCoherence Score: ', coherence_lda)

!pip install pandas=='1.2.0'

"""**Visualization of the model performance**"""

pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(ldamodel, corpus, dictionary)
vis

NUM_TOPICS = 12
ldamodel1 = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel1.save('model12.gensim')
topics = ldamodel1.print_topics(num_words=4)
for topic in topics:
    print(topic)

#Computing Perplexity
print('\nPerplexity: ', ldamodel1.log_perplexity(corpus))

# Computing Coherence Score
coherence_ldamodel1 = CoherenceModel(model=ldamodel1, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_lda1 = coherence_ldamodel1.get_coherence()
print('\nCoherence Score: ', coherence_lda1)

"""**LDA(BoW) number of topics = 12**"""

pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(ldamodel1, corpus, dictionary)
vis

"""**LDA(BoW) number of topics = 14**"""

NUM_TOPICS = 14
ldamodel2 = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel2.save('model14.gensim')
topics = ldamodel2.print_topics(num_words=4)
for topic in topics:
    print(topic)

#Computing Perplexity
print('\nPerplexity: ', ldamodel2.log_perplexity(corpus))

# Computing Coherence Score
coherence_ldamodel2 = CoherenceModel(model=ldamodel2, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_lda2 = coherence_ldamodel2.get_coherence()
print('\nCoherence Score: ', coherence_lda2)

pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(ldamodel2, corpus, dictionary)
vis

"""**LDA(BoW) number of topics = 16**"""

NUM_TOPICS = 16
ldamodel3 = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel3.save('model16.gensim')
topics = ldamodel3.print_topics(num_words=4)
for topic in topics:
    print(topic)

#Computing Perplexity
print('\nPerplexity: ', ldamodel3.log_perplexity(corpus))

# Computing Coherence Score
coherence_ldamodel3 = CoherenceModel(model=ldamodel3, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_lda3 = coherence_ldamodel3.get_coherence()
print('\nCoherence Score: ', coherence_lda3)

pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(ldamodel3, corpus, dictionary)
vis

"""**LDA(BoW) number of topics = 18**"""

NUM_TOPICS = 18
ldamodel4 = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel4.save('model18.gensim')
topics = ldamodel4.print_topics(num_words=4)
for topic in topics:
    print(topic)

#Computing Perplexity
print('\nPerplexity: ', ldamodel4.log_perplexity(corpus))

# Computing Coherence Score
coherence_ldamodel4 = CoherenceModel(model=ldamodel4, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_lda4 = coherence_ldamodel4.get_coherence()
print('\nCoherence Score: ', coherence_lda4)

pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(ldamodel4, corpus, dictionary)
vis

"""we can see that the model performance is getting worse with increase in the number of topics. Based on the coherence score and the tradeoff with the perplexity score, the model with number of topics 10 and 12 perform better than the rest with higher number of topics

**Performing tf-idf instead of bag of words and checking the model performance for the number of topics 10, 12 and 14**
"""

from gensim import corpora, models
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
from pprint import pprint
for doc in corpus_tfidf:
    pprint(doc)
    break

"""**LDA(TF-IDF) number of topics = 14**"""

ldamodel_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=14, id2word=dictionary, passes=15, workers=4)
for idx, topic in ldamodel_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))

#Computing Perplexity
print('\nPerplexity: ', ldamodel_tfidf.log_perplexity(corpus))

# Computing Coherence Score
coherence_ldamodel5 = CoherenceModel(model=ldamodel_tfidf, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_lda5 = coherence_ldamodel5.get_coherence()
print('\nCoherence Score: ', coherence_lda5)

pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(ldamodel_tfidf, corpus, dictionary)
vis

"""**LDA(TF-IDF) number of topics = 12**"""

ldamodel_tfidf1 = gensim.models.LdaMulticore(corpus_tfidf, num_topics=12, id2word=dictionary, passes=15, workers=4)
for idx, topic in ldamodel_tfidf1.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))

#Computing Perplexity
print('\nPerplexity: ', ldamodel_tfidf1.log_perplexity(corpus))

# Computing Coherence Score
coherence_ldamodel6 = CoherenceModel(model=ldamodel_tfidf1, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_lda6 = coherence_ldamodel6.get_coherence()
print('\nCoherence Score: ', coherence_lda6)

pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(ldamodel_tfidf1, corpus, dictionary)
vis

"""**LDA(TF-IDF) number of topics = 10**"""

ldamodel_tfidf2 = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=15, workers=4)
for idx, topic in ldamodel_tfidf2.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))

#Computing Perplexity
print('\nPerplexity: ', ldamodel_tfidf2.log_perplexity(corpus))

# Computing Coherence Score
coherence_ldamodel7 = CoherenceModel(model=ldamodel_tfidf2, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_lda7 = coherence_ldamodel7.get_coherence()
print('\nCoherence Score: ', coherence_lda7)

pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(ldamodel_tfidf2, corpus, dictionary)
vis

"""With the tf-idf LDA model, based on the coherence score and the map we can intrepret that the model with the number of topics 12 performs better than the rest with good coherence score and the non-overlapping big circles.

**Implementation using LDAMallet**
"""

#environment setup for executing the Mallet LDA
import os       
def install_java():
  !apt-get install -y openjdk-8-jdk-headless -qq > /dev/null      
  os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"    
  !java -version       #check java version
install_java()

!wget http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip
!unzip mallet-2.0.8.zip

"""**Number of Topics: 10**"""

os.environ['MALLET_HOME'] = '/content/mallet-2.0.8'
mallet_path = '/content/mallet-2.0.8/bin/mallet'
ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=10, id2word=dictionary)

print(ldamallet.show_topics(formatted=False))

# Compute Coherence Score
coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_ldamallet = coherence_model_ldamallet.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet)

"""**Number of Topics: 12**"""

ldamallet1 = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=12, id2word=dictionary)
print(ldamallet1.show_topics(formatted=False))

# Compute Coherence Score
coherence_model_ldamallet1 = CoherenceModel(model=ldamallet1, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_ldamallet1 = coherence_model_ldamallet1.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet1)

"""**Number of Topics: 14**"""

ldamallet2 = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=14, id2word=dictionary)
print(ldamallet2.show_topics(formatted=False))

# Compute Coherence Score
coherence_model_ldamallet2 = CoherenceModel(model=ldamallet2, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_ldamallet2 = coherence_model_ldamallet2.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet2)

"""**Number of Topics: 16**"""

ldamallet3 = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=16, id2word=dictionary)
print(ldamallet3.show_topics(formatted=False))

# Compute Coherence Score
coherence_model_ldamallet3 = CoherenceModel(model=ldamallet3, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_ldamallet3 = coherence_model_ldamallet3.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet3)

"""**Number of Topics: 18**"""

ldamallet4 = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=18, id2word=dictionary)
print(ldamallet4.show_topics(formatted=False))

# Compute Coherence Score
coherence_model_ldamallet4 = CoherenceModel(model=ldamallet4, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_ldamallet4 = coherence_model_ldamallet4.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet4)

"""**Number of Topics: 20**"""

ldamallet5 = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=dictionary)
print(ldamallet5.show_topics(formatted=False))

# Compute Coherence Score
coherence_model_ldamallet5 = CoherenceModel(model=ldamallet5, texts=processed_data, dictionary=dictionary, coherence='c_v')
coherence_ldamallet5 = coherence_model_ldamallet5.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet5)

"""Based on the coherence value, it is observed that the LDAMallet model with number of topics=10 performs better"""

def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=dictionary)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values

model_list, coherence_values = compute_coherence_values(dictionary=dictionary, corpus=corpus, texts=processed_data, start=2, limit=40, step=2)

"""**To check which number would be optimal number of topics for LDAMallet**"""

limit=40; start=2; step=2;
x = range(start, limit, step)
plt.plot(x, coherence_values)
plt.xlabel("Num Topics")
plt.ylabel("Coherence score")
plt.legend(("coherence_values"), loc='best')
plt.show()

for m, cv in zip(x, coherence_values):
    print("Num Topics =", m, " has Coherence Value of", round(cv, 4))

"""Displaying the topics which from the optimal model with number of topics=10 and 12"""

optimal_model = model_list[4]
model_topics = optimal_model.show_topics(formatted=False)
pprint(optimal_model.print_topics(num_words=10))

optimal_model = model_list[5]
model_topics = optimal_model.show_topics(formatted=False)
pprint(optimal_model.print_topics(num_words=10))

"""**To check the performance of the models(LDA(BoW and TF-IDF) and LDAMallet)on the unseen data**

LDA Model(TF-IDF) with number of topics = 12
"""

unseendata = 'Aerodynamic interaction between propellers of a distributed-propulsion system in forward flight'
corpust = dictionary.doc2bow(preprocess(unseendata))
for index, score in sorted(ldamodel_tfidf1[corpust], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, ldamodel_tfidf1.print_topic(index, 2)))

"""LDA Model(TF-IDF) with number of topics = 14"""

unseen_data = 'Aerodynamic interaction between propellers of a distributed-propulsion system in forward flight'
corpus_t = dictionary.doc2bow(preprocess(unseen_data))
for index, score in sorted(ldamodel_tfidf[corpus_t], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, ldamodel_tfidf.print_topic(index, 2)))

"""LDA Model(BoW) with number of topics = 12"""

unseen_data1 = 'Aerodynamic interaction between propellers of a distributed-propulsion system in forward flight'
corpus_t1 = dictionary.doc2bow(preprocess(unseen_data))
for index, score in sorted(ldamodel1[corpus_t1], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, ldamodel1.print_topic(index, 2)))

"""LDAMallet with number of topics = 12"""

unseen_data2 = 'Aerodynamic interaction between propellers of a distributed-propulsion system in forward flight'
corpus_t2 = dictionary.doc2bow(preprocess(unseen_data))
for index, score in sorted(ldamallet1[corpus_t2], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, ldamallet1.print_topic(index, 2)))

"""LDAMallet with number of topics = 10"""

unseen_data3 = 'Aerodynamic interaction between propellers of a distributed-propulsion system in forward flight'
corpus_t3 = dictionary.doc2bow(preprocess(unseen_data))
for index, score in sorted(ldamallet[corpus_t3], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, ldamallet.print_topic(index, 2)))

"""**Unseen data 2**

LDA(TF-IDF) with number of topics = 14
"""

test_data = 'Turbulence Model Could Help Design Aircraft Capable of Handling Extreme Scenarios'
corpus_test = dictionary.doc2bow(preprocess(test_data))
for index, score in sorted(ldamodel_tfidf[corpus_test], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, ldamodel_tfidf.print_topic(index, 2)))

"""LDA(BoW) with number of topics = 12"""

test_data1 = 'No One Can Explain Why Planes Stay in the Air'
corpus_test1 = dictionary.doc2bow(preprocess(test_data1))
for index, score in sorted(ldamodel1[corpus_test1], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, ldamodel1.print_topic(index, 2)))

test_data2 = 'Turbulence Model Could Help Design Aircraft Capable of Handling Extreme Scenarios'
corpus_test2 = dictionary.doc2bow(preprocess(test_data2))
for index, score in sorted(ldamodel1[corpus_test2], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, ldamodel1.print_topic(index, 2)))

test_data3 = 'Zero emissions hydrogen plane test was part powered by fossil fuels'
corpus_test3 = dictionary.doc2bow(preprocess(test_data3))
for index, score in sorted(ldamodel1[corpus_test3], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, ldamodel1.print_topic(index, 2)))

"""LDAMallet with number of topics = 12"""

test_data4 = 'Turbulence Model Could Help Design Aircraft Capable of Handling Extreme Scenarios'
corpus_test4 = dictionary.doc2bow(preprocess(test_data4))
for index, score in sorted(ldamallet1[corpus_test4], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, ldamallet1.print_topic(index, 2)))

"""Overall, it is seen that the LDA(BoW) model with 12 topics performed well but the LDA(TF-IDF) model with number of topics=12 and 14 performed better than the former. LDAMallet with number of topics 10 and 12 are performing well compared to the LDA models."""