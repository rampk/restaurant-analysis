import mysql.connector as connection
import pandas as pd
import numpy as np
import contractions
from unidecode import unidecode
import re
from bs4 import BeautifulSoup
import spacy
from nltk.corpus import stopwords


def read_data():
    try:
        mydb = connection.connect(host="localhost", database = 'yelp_review',user="db_user", passwd="P@s$w0rd123!",use_pure=True)
        query = "SELECT * from restaurant where city='Burnaby';"
        df = pd.read_sql(query,mydb)
        return df

    except Exception as e:
        print(str(e))

    finally:
        mydb.close()


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

# Lemmatization
def lemmatizer(text):
    nlp = spacy.load('en_core_web_sm')
    return " ".join([word.lemma_ for word in nlp(text)])


if __name__ == '__main__':
    
    # Read the data
    df_review = read_data()
    # Decode the tweet_text
    df_review = decode_string(df_review)
    # Clean the data
    df_review = clean_data(df_review)
    # Remove stop_words
    df_review['text'] = df_review['text'].apply(remove_stop_words)
    # Lemmatization
    df_review['text'] = df_review['text'].apply(lemmatizer) 

