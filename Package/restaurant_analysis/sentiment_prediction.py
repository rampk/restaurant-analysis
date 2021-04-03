import pkgutil
import pickle

model_pipeline = pkgutil.get_data('restaurant_analysis', 'bin/model_pipeline.pkl')
review_prediction = pickle.loads(model_pipeline)
