import pkgutil
import pickle


class SentimentPredictor:
    def __init__(self):
        model_pipeline = pkgutil.get_data('restaurant_analysis', 'bin/model_pipeline.pkl')
        self.review_prediction = pickle.loads(model_pipeline)
        self.prediction = []
        self.acceptance_rate = 0

    def predict(self, x):
        self.prediction = self.review_prediction.predict(x)
        return self.prediction

    def acceptance(self):
        self.acceptance_rate = sum(self.prediction)/len(self.prediction)