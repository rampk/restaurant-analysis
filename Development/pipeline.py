# Import required packages for pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.compose import ColumnTransformer

# Constructing a custom tranformer for data preprocessing 
class DecodeTransformer(BaseEstimator,TransformerMixin):
    def __init__(self):
        pass

    def fit(self,X,y=None):
        return self
    
    def transform(self,X,y=None):
        return X.decode('utf-8')

decode_transformer = DecodeTransformer() 
data_preprocess = Pipeline([('decode_transformer',decode_transformer)]
