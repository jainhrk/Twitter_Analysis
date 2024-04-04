# -*- coding: utf-8 -*-
"""News-Article-Api's and Topic Modeling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VvP0F_CmHPr6ePXun7bWVs8gEjkRHnzo
"""

import pprint
import requests 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
import re
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
nltk.download('omw-1.4')
nltk.download('wordnet')
from bs4 import BeautifulSoup
from nltk import word_tokenize

secret = '544677c4098f4f00b25e2a72a7e5c904'

url = 'https://newsapi.org/v2/everything?'

parameters = {
    'q': 'NBA LEAGUE 2021-22', # query phrase
    'pageSize': 80,  # maximum is 100
    'apiKey': secret # your own API key
}

# Make the request
response = requests.get(url, params=parameters)

# Convert the response to JSON format and pretty print it
response_json = response.json()
pprint.pprint(response_json)

for i in response_json['articles']:
    print(i['title'])

# Create an empty string
text_combined = ''
# Loop through all the headlines and add them to 'text_combined'
for i in response_json['articles']:
    text_combined += i['title'] + ' ' # add a space after every headline, so the first and last words are not glued together
# Print the first 300 characters to screen for inspection
print(text_combined[0:200])

text_combined

def preprocess_text(raw_text):
  corpus=raw_text
  corpus=corpus.lower()
  corpus = re.sub(r'[^\w\s]','', corpus)
  corpus = re.sub('\[.*?\]', '', corpus)
  corpus = re.sub('https?://\S+|www\.\S+', '', corpus)
  corpus = re.sub('<.*?>+', '', corpus)
  corpus = re.sub('\n', '', corpus)
  corpus = re.sub('\w*\d\w*', '', corpus)
  words=nltk.word_tokenize(corpus)
  word_tokens=word_tokenize(corpus)
  stop_words=set(stopwords.words('english'))
  
  filtered_words=[]
  for w in word_tokens:
   if w not in stop_words:
     filtered_words.append(w)
  
  lemmatizer=WordNetLemmatizer()
  lemma_words = []

  for w in filtered_words:
    rootWord = lemmatizer.lemmatize(w, pos=wordnet.VERB)
    lemma_words.append(rootWord)
  
  return lemma_words

clean_text_titles=preprocess_text(text_combined)

def freq_dist(clean_text):
  frequency_dist = nltk.FreqDist(clean_text)
  large_words = dict((k,v) for k,v in frequency_dist.items() if len(k) > 3)
  freq_dist = nltk.FreqDist(large_words)
  print(freq_dist)
  freq_dist.plot(20,cumulative=False)
  wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate_from_frequencies(freq_dist)
  plt.figure()
  plt.imshow(wordcloud, interpolation="bilinear")
  plt.axis("off")
  plt.show()
  freq_dist1 = freq_dist.most_common(30)
  x = [item[0] for item in freq_dist1]
  y = [item[1] for item in freq_dist1]

  # Creates a bar chart
  colors = ['blue', 'red', 'green', 'orange', 'purple', 'pink', 'gray', 'brown', 'black', 'yellow']
  plt.bar(x, y, color=colors)


  # Chart title and axis labels
  plt.title("Top 20 Content-words by Frequency")
  plt.xlabel("Words")
  plt.ylabel("Frequency")

  # Rotate x-axis labels for better readability
  plt.xticks(rotation=90)
  plt.grid(axis="y", linestyle="--", alpha=0.7)

  # Display chart
  plt.show()

freq_dist(clean_text_titles)

"""News Content"""

# Create an empty string
text_combined_content= ''
# Loop through all the headlines and add them to 'text_combined' 
for i in response_json['articles']:
    text_combined_content += i['content'] + ' ' # add a space after every headline, so the first and last words are not glued together
# Print the first 300 characters to screen for inspection
print(text_combined_content[0:300])

text_combined_content

clean_text_content=preprocess_text(text_combined_content)

freq_dist(clean_text_content)

"""***TOPIC MODELING***"""

!pip install gensim

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from string import punctuation
from nltk.tokenize import word_tokenize
from collections import Counter
import operator
import numpy as np
import nltk
from textblob import TextBlob
import string
from gensim.models.ldamodel import LdaModel
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim.models.lsimodel import LsiModel
from gensim.models.coherencemodel import CoherenceModel
from gensim import corpora
from pprint import pprint
import seaborn as sns

l1=[clean_text_content]
# Creating the dictionary id2word from our cleaned word list doc_clean
dictionary = corpora.Dictionary(l1)

# Creating the corpus
doc_term_matrix = [dictionary.doc2bow(doc) for doc in l1]

def find_no_of_models(doc_term_matrix):
  topics=[2,3,4,5,6,7,8,9,10]
  perplexity=[]
  coherence=[]
  for i in range(2,11):
    ldamodel = LdaModel(corpus=doc_term_matrix, num_topics=i,id2word=dictionary, random_state=20, passes=30)
    perplexity_lda = ldamodel.log_perplexity(doc_term_matrix)
    coherence_model_lda = CoherenceModel(model=ldamodel, texts=l1, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    #topics.append("No of Topics:" + str(i))
    perplexity.append(perplexity_lda)
    coherence.append(coherence_lda)
    print(perplexity)
    print(coherence)

find_no_of_models(doc_term_matrix)

ldamodel_final = LdaModel(corpus=doc_term_matrix, num_topics=9,id2word=dictionary, random_state=20, passes=30)

# printing the topics
pprint(ldamodel_final.print_topics())
from gensim.models.coherencemodel import CoherenceModel

# Compute Perplexity
perplexity_lda = ldamodel_final.log_perplexity(doc_term_matrix)
print('\nPerplexity: ', perplexity_lda)  


# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=ldamodel_final, texts=l1, dictionary=dictionary, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)

from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors

#cols = [color for name, color in mcolors.XKCD_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'
cols = ['red', 'green', 'blue', 'orange', 'purple', 'yellow', 'pink', 'teal', 'grey']
color_func=lambda *args, **kwargs: cols[i % len(cols)]

cloud = WordCloud(stopwords=stopwords,
                  background_color='white',
                  width=3000,
                  height=2100,
                  max_words=8,
                  colormap='tab10',
                  color_func=lambda *args, **kwargs: cols[i],
                  prefer_horizontal=1.0)

topics = ldamodel_final.show_topics(formatted=False)

fig, axes = plt.subplots(3, 3, figsize=(10,10), sharex=True, sharey=True)

for i, ax in enumerate(axes.flatten()):
    fig.add_subplot(ax)
    topic_words = dict(topics[i][1])
    cloud.generate_from_frequencies(topic_words, max_font_size=500)
    plt.gca().imshow(cloud)
    plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=20))
    plt.gca().axis('off')


plt.subplots_adjust(wspace=0, hspace=0)
plt.axis('off')
plt.margins(x=0, y=0)
plt.tight_layout()
plt.show()

import requests
from urllib.parse import urlencode


def GetArticles(query, secret, url):
    parameters = {
        'q': query,
        'apiKey': secret,
        'pageSize': 100,
        'language': 'en'
    }

    query_url = url + urlencode(parameters)
    response = requests.get(query_url)

    urls = []
    if response.ok:
        articles = response.json()['articles']
        for article in articles:
            urls.append(article['url'])
    else:
        print(f"Failed to get articles with error {response.status_code}")
        
    return urls

def DataPreprocessing(urls):
    stops = stopwords.words("english")
    lemmatizer = WordNetLemmatizer() #Create Lemmtizer object
    fdist =nltk.FreqDist() #Create frequency distribution object
    webpages=[] #Create an empty list for clean text bodys
    for i in urls:
        CleanedWords =[] #Empty list to hold all clean words
        webpage =requests.get(i).text #Make request and get webpage contents
        soup = BeautifulSoup(webpage, "html.parser") #Create beautiful soup object for article

        siteText=""
        for j in soup.find_all("p"): #Find all paragraph tags within the html page
            siteText += j.get_text() #Get text from each paragraph tag in document and append to 'text' variable


        siteText = re.sub(r"[^a-zA-Z0-9]+"," ", siteText) #Remove all none alphanumeric characters
        
        siteText = siteText.lower() #Convert to lowercase
        words = nltk.word_tokenize(siteText)

        
        for i in words:
            if i not in stops: #If the word isnt a stop word then lemmatize it and add it to the list of cleaned words
                i = lemmatizer.lemmatize(i, pos=wordnet.NOUN)
                CleanedWords.append(i)
                fdist[i] +=1
                
        webpages.append(CleanedWords) #Append list of cleaned words to webpages list
    return fdist, webpages

def Visualisations(fdist):
    fdist.plot(30) #Plotting Articles frequency distribution
    
    #Plotting word cloud for articles combined.
    wordcloud = WordCloud(max_font_size=50, max_words = 100, background_color="white").generate_from_frequencies(fdist)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

def TopicModel(webpages, start, end): #WARNING THIS TAKES A LONG TIME TO CALCULATE
    coherences =[] #Create empty list of coherences for plotting
    bestVal = 0 #Placeholder to hold number of topics with current best coherence score
    bestCoh = 0# Placeholder to hold current best coherence score
    
    for i in range(start,end+1):
        model=create_gensim_lsa_model(webpages, i) #Create LSI model
        cm = CoherenceModel(model=model, texts=webpages, coherence='c_v') #Create coherence model
        coherence = cm.get_coherence() #Compute coherence for previously created LSI model
        
        if coherence > bestCoh: #Check if new best coherence model has been found
            bestVal =i
            bestCoh = coherence
        coherences.append(coherence) #Save coherence
    
    #Plot line plot of coherence scores and number of topics
    p = sns.lineplot(x=[x for x in range (start, end+1)], y=coherences)
    p.set(xlabel='Number of topics', ylabel='Coherence score')
    plt.show()
    
    #Return best number of topics
    return bestVal



def GenerateTopics(webpages, bestVal):
    #Create another copy of best LSI model with best numbe of topics
    model=create_gensim_lsa_model(webpages, bestVal)
    
    #Itterate through topics found
    for i in model.show_topics(bestVal):
        #String Manipulate topics to print out the word makeup of each topic
        for j in i[1].split(" + "):
            vals = j.split("*")
            vals[1] = vals[1].replace('"','')
            print("%s & %s \\\\"%(vals[1], vals[0]))
        print()    

def prepare_corpus(doc_clean):
    #Create a corpora dictionary out of the submitted list of article texts
    dictionary = corpora.Dictionary(doc_clean)
    #Create a term matrix for each of the webpages
    term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    return dictionary, term_matrix

def create_gensim_lsa_model(doc_clean, number_of_topics):
    dictionary, doc_term_matrix = prepare_corpus(doc_clean) 
    #Create LSImodel using supplied documents and specified number of topics.
    ldamodel = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word=dictionary)
    return ldamodel

def preprocessing(doc_set):
    #Use regex to work tokenize
    tokenizer= RegexpTokenizer(r"\W+")
    stops = stopwords.words("english")
    lemmatizer = WordNetLemmatizer() #Create Lemmtizer object
    texts = []
    for i in doc_set: #For i in doc_set where doc_set is a list of words that were previously text but have been word tokenized
        raw = i.lower() #Convert to lowercase
        tokens = tokenizer.tokenize(raw) 
        stopped_tokens = [i for i in tokens if not i in stops] #Remove Stopwords
        Lemmed_tokens = [lemmatizer.lemmatize(i, pos=wordnet.VERB) for i in stopped_tokens] #Lemmatize words
        texts.append(Lemmed_tokens)
    return texts

secret = "544677c4098f4f00b25e2a72a7e5c904"
url = 'https://newsapi.org/v2/everything?'

#harcoded but customisable query
query = "NBA LEAGUE 2021-22"
#minimum number of topics to check
TopicMinimumAmount = 10
#maximum number of topics to check
TopicMaximumAmount = 13

urls = GetArticles(query, secret, url)
fdist, webpages =DataPreprocessing(urls)
Visualisations(fdist)

bestVal = TopicModel(webpages, TopicMinimumAmount, TopicMaximumAmount)
GenerateTopics(webpages, bestVal)