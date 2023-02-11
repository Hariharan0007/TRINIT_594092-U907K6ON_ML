import pickle
import pandas as pd
from sklearn.metrics import accuracy_score
import requests

api_key = 'a41cf401d26849f7bf0133021231102'

model = pickle.load(open('model.pkl', 'rb'))

dataset = pd.read_csv('Crop_recommendation.csv')
predict_data = dataset.iloc[0:1, 0:7].values

result = model.predict(predict_data)

accuracy = accuracy_score(dataset.iloc[0:1, 7].values, result)
print(accuracy)

def map_state_to_soil(state):
    state_wise_soil = pd.read_csv('soil/npk.csv')
    for i in range(0, len(state_wise_soil)):
        if state_wise_soil.iloc[i, 0] == state:
            return state_wise_soil.iloc[i, 1]
    return 0

def getNPK(state):
    npk = pd.read_csv('soil/npk.csv')
    for i in range(0, len(npk)):
        if npk.iloc[i, 0] == state:
            return (npk.iloc[i, 2], npk.iloc[i, 3], npk.iloc[i, 4])
        
    return (0, 0, 0)

def getWeather(district):
    link = "http://api.weatherapi.com/v1/current.json?key=" + api_key + "&q=" + district + "&aqi=no"
    response = requests.get(link)
    temperature = response.json()['current']['temp_c']
    humidity = response.json()['current']['humidity']
    
    return (temperature, humidity)

def getPH(state):
    ph = pd.read_csv('water/ph.csv', encoding='unicode_escape')
    for i in range(0, len(ph)):
        if ph.iloc[i, 2] == state:
            return ph.iloc[i, 5]
        
    return 0

def getRainfall(district):
    return 40
        
def getList(l):
    # convert elements of list to float
    for i in range(0, len(l)):
        for j in range(0, len(l[i])):
            l[i][j] = float(l[i][j])
    crops = model.predict(l)
    
    return crops
    
def main(state, district):
    state = state.upper()
    
    (N, P, K) = getNPK(state)
    
    (temperature, humidity) = getWeather(district)
    
    ph = getPH(state)
    rainfall = getRainfall(district)
    
    predict_data = [[N, P, K, temperature, humidity, ph, rainfall]]
    return str(getList(predict_data))
    
main('Tamil Nadu', 'Ooty') # mothbeans
