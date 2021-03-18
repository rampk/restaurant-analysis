# Importing required libraries
import mysql.connector as connection
import pandas as pd
import numpy as np
import contractions
from unidecode import unidecode
import re
from bs4 import BeautifulSoup
import spacy
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer 
import pickle
from sklearn.model_selection import StratifiedShuffleSplit
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


# Reading the data from DB
def read_data():
    try:
        mydb = connection.connect(host="localhost", database = 'yelp_review',user="db_user", passwd="P@s$w0rd123!",use_pure=True)
        query = "SELECT * from restaurant"
        df = pd.read_sql(query,mydb)
        return df

    except Exception as e:
        print(str(e))

    finally:
        mydb.close()


# Creating test set
def test_data_generation(df_review):
    split = StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=7)

    for train,test in split.split(df_review,df_review['stars']):
        train_data = df_review.iloc[train]
        test_data = df_review.iloc[test]

    test_data.to_csv('Data/test_data.csv', index=False)
    return train_data


# Decoding the string
def decode_string(df):
    df['text'] = df['text'].apply(lambda x: x.decode('utf-8'))
    return df


# Removing the HTML tags
def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator=" ")
    return text


# Removing the URLS from text
def remove_links(text):
    text = re.sub(r'https?:\/\/.*[ ]*', '', text)
    return text


# Converting non-ascii
def transform_nonascii(text):
    return ''.join(char for char in text if ord(char) < 128)
    return unidecode(text)


# Removing numbers
def remove_numbers(text):
    return re.sub(r'[0-9]+', '', text)


# Removing slashes
def remove_slash(text):
    return re.sub(r'[\n,\b,\t]', '', text)


# Removing contractions
def remove_contractions(text):
    return contractions.fix(text)


# Removing non-alphanumerics:
def remove_nonalpha(text):
    text = re.sub(r'[^\w]', ' ', text)
    text = re.sub(r'_', '', text)
    return text


# Removing words with less words
def remove_less_characters(text):
    return re.sub(r'\b\w{1,2}\b','', text)


# Unwanted spaces:
def remove_space(text):
    return re.sub(r' +', ' ', text)


# Cleaning the text
def clean_data(df):
    df['text'] = df['text'].apply(remove_html_tags)
    df['text'] = df['text'].apply(transform_nonascii)
    df['text'] = df['text'].apply(remove_numbers)
    df['text'] = df['text'].apply(remove_links)
    df['text'] = df['text'].apply(remove_slash)
    df['text'] = df['text'].apply(remove_contractions)
    df['text'] = df['text'].apply(remove_nonalpha)
    df['text'] = df['text'].apply(remove_less_characters)
    df['text'] = df['text'].apply(remove_space)
    df['text'] = df['text'].str.lower()

    return df


# Stop words removal
def remove_stop_words(text):

    removed_list = []

    for token in text.split():

        if token not in stopwords.words('english'):
            removed_list.append(token)


    return " ".join(removed_list)


# Stemming
def stemming(text):
    ps = PorterStemmer()
    return " ".join([ps.stem(word) for word in word_tokenize(text)])


# Converting lables to three categories
def process_label(label):
    for idx in range(len(label)):
        # Positive if stars are above 4
        if label[idx] >= 4:
            label[idx] = 1
        # Negative if starts are below 2
        elif label[idx] <= 2:
            label[idx] = -1
        # Neutral if starts is 3
        else:
            label[idx] = 0

    return label


if __name__ == '__main__':
    
    # Read the data
    print('Reading the data')
    df_review = read_data()
    # Generate Test data
    print('Spliting test and train data')
    df_review  =  test_data_generation(df_review)
    # Decode the tweet_text
    df_review = decode_string(df_review)
    # Clean the data
    print('Cleaning the text')
    df_review = clean_data(df_review)
    # Remove stop_words
    print('Removing the stopwords')
    df_review['text'] = df_review['text'].apply(remove_stop_words)
    # Stemming 
    print('Stemming the text')
    df_review['text'] = df_review['text'].apply(stemming)


    # Vectorizing
    print('Vectorizing the text')
    vectorizer = CountVectorizer()

    train_X = vectorizer.fit_transform(df_review['text'])

    train_y = df_review['stars'].to_numpy()
    train_y = process_label(train_y)

    # Pickling the process data and vectorizer object
    with open('binfiles/vectorizer.pkl','wb') as file:
        pickle.dump(vectorizer,file)

    with open('binfiles/train_data.pkl','wb') as file:
        pickle.dump(train_X,file)

    with open('binfiles/train_label.pkl','wb') as file:
        pickle.dump(train_y,file)



