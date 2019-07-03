import pickle
import sys
import re

import pandas as pd
from numpy import array

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from statistics import mode





class predictor():
    def __init__(self, dir_path = '', cl_name = 'lsvc'):
        #load tfidf
        with open(dir_path + 'tfidf.pkl','rb') as file:
            self.tfidf = pickle.load(file)

        #load classifier
        with open(dir_path + cl_name + '.pkl','rb') as file:
            self.cl = pickle.load(file)


    def pred(self, dox):
        feats = self.tfidf.transform(dox)
        df = pd.DataFrame(feats.todense(), columns = self.tfidf.get_feature_names())
        preds = self.cl.predict(df)
        try:
            return mode(preds)
        except:
            return 'centre'
            

    def classify(self, tweets, resolution = False):
        if not resolution:
            flag = False
            resolution = 1
        else:
            flag = True

        res = []
        while resolution < len(tweets):
            dox = []
            c = 0
            l = []
            for i in tweets:
                c+=1
                l.append(i)
                if c%resolution == 0:
                    dox.append(clean(' '.join(l),True,True))
                    l = []

            dox.append(clean(' '.join(l),True,True))


            res.append(self.pred(dox))
            if flag:
                break

            resolution *= 2
            
        try:
            return mode(res)
        except:
            return 'centre'
      
####################################################################################  

def clean(text, remove_stopwords=False, stem_words=False):

    text = text.lower().split()

    if remove_stopwords:
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
    
    text = " ".join(text)
    
    # Clean the text
    #print(text)
    text = re.sub(r"b'rt",'',text)
    text = re.sub(r"http.+?\s",'',text)
    text = re.sub(r"@.+?\s",'',text)
    text = re.sub(r"[0-9]+",'',text)
    text = re.sub(r"x[a-z][0-9]",'',text)
    text = re.sub(r"x[a-z]",'',text)
    text = re.sub(r"x",'',text)
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    
      
    # Optionally, shorten words to their stems
    if stem_words:
        text = text.split()
        stemmer = SnowballStemmer('english')
        stemmed_words = [stemmer.stem(word) for word in text]
        text = " ".join(stemmed_words)
    
    '''
    tokens = word_tokenize(text)
    pos_text = pos_tag(tokens)
    new_text = ' '.join([i[0]+'-'+i[1] for i in pos_text])
    '''
    
    # Return a list of words
    return(text)