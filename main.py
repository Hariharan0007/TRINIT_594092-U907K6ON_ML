import pickle
import pandas as pd
from sklearn.metrics import accuracy_score

model = pickle.load(open('model.pkl', 'rb'))

dataset = pd.read_csv('Crop_recommendation.csv')
predict_data = dataset.iloc[0:1, 0:7].values

result = model.predict(predict_data)

accuracy = accuracy_score(dataset.iloc[0:1, 7].values, result)
print(accuracy)
