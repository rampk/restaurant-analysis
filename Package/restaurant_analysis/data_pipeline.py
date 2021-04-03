# Import required packages for pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

# Import required libraries
import pandas as pd
from bs4 import BeautifulSoup
import re
import contractions
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import pkgutil
import pickle


# Constructing a custom transformer for data preprocessing
class CleanTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self,X,y=None):
        return self

    # Removing the HTML tags
    def remove_html_tags(self,text):
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text(separator=" ")
        return text

    # Removing the URLS from text
    def remove_links(self,text):
        text = re.sub(r'https?:\/\/.*[ ]*', '', text)
        return text

    # Converting non-ascii
    def transform_nonascii(self,text):
        return ''.join(char for char in text if ord(char) < 128)

    # Removing numbers
    def remove_numbers(self,text):
        return re.sub(r'[0-9]+', '', text)

    # Removing slashes
    def remove_slash(self,text):
        return re.sub(r'[\n,\b,\t]', '', text)

    # Removing contractions
    def remove_contractions(self,text):
        return contractions.fix(text)

    # Removing non-alphanumerics:
    def remove_nonalpha(self,text):
        text = re.sub(r'[^\w]', ' ', text)
        text = re.sub(r'_', '', text)
        return text

    # Removing words with less words
    def remove_less_characters(self,text):
        return re.sub(r'\b\w{1,2}\b', '', text)

    # Unwanted spaces:
    def remove_space(self,text):
        return re.sub(r' +', ' ', text)

    def transform(self,X,y=None):
        X = X.apply(self.remove_html_tags)
        X = X.apply(self.transform_nonascii)
        X = X.apply(self.remove_numbers)
        X = X.apply(self.remove_links)
        X = X.apply(self.remove_slash)
        X = X.apply(self.remove_contractions)
        X = X.apply(self.remove_nonalpha)
        X = X.apply(self.remove_less_characters)
        X = X.apply(self.remove_space)
        X = X.str.lower()
        return X

class StopWordsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self,X,y=None):
        return self

    # Stop words removal
    def remove_stop_words(self,text):
        removed_list = []
        for token in text.split():
            if token not in stopwords.words('english'):
                removed_list.append(token)

        return " ".join(removed_list)

    def transform(self,X,y=None):
        return X.apply(self.remove_stop_words)


class StemmingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self,X,y=None):
        return self

    # Stemming
    def stemming(self,text):
        ps = PorterStemmer()
        return " ".join([ps.stem(word) for word in word_tokenize(text)])

    def transform(self,X,y=None):
        return X.apply(self.stemming)


clean_transformer = CleanTransformer()
stop_words = StopWordsTransformer()
stemming_transformer = StemmingTransformer()

vectorizer_pkl = pkgutil.get_data('restaurant_analysis', 'bin/vectorizer.pkl')
vectorizer = pickle.loads(vectorizer_pkl)
model_pkl = pkgutil.get_data('restaurant_analysis', 'bin/model_lr.pkl')
model = pickle.loads(model_pkl)


model_pipeline = Pipeline([('clean_transformer', clean_transformer), ('stop_words', stop_words),
                           ('stemming_transformer', stemming_transformer), ('vectorizer', vectorizer),
                           ('model', model)])


#with open('model_pipeline.pkl', 'wb') as file:
#    pickle.dump(model_pipeline, file)