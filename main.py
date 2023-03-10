import pickle
import pandas as pd
from sklearn.metrics import accuracy_score
import requests
import datetime
import fastapi

app = fastapi.FastAPI()

api_key = 'a41cf401d26849f7bf0133021231102'

model = pickle.load(open('model.pkl', 'rb'))

dataset = pd.read_csv('Crop_recommendation.csv')
predict_data = dataset.iloc[0:1, 0:7].values

result = model.predict(predict_data)

accuracy = accuracy_score(dataset.iloc[0:1, 7].values, result)
print(accuracy)

df = pd.read_csv('Crop_recommendation.csv')

# give a list of crops
crops = df['label'].unique()

# segregate similar crops according to paramaters
# N, P, K, temperature, humidity, ph, rainfall
# if the parameters are in the range of the crop, then it is a similar crop
# get avg N, P, K, temperature, humidity, ph, rainfall for each crop
avg = {}
for crop in crops:
    avg[crop] = df[df['label'] == crop].mean()

similar_crops = {}
for crop in crops:
    similar_crops[crop] = []
    
    # if the combined value of N, P, K, temperature, humidity, ph, rainfall is in the range of the crop, then it is a similar crop
    for crop2 in crops:
        if crop2 == crop:
            continue
        if 0.9 * (avg[crop]['N'] + avg[crop]['P'] + avg[crop]['K'] + avg[crop]['temperature'] + avg[crop]['humidity'] + avg[crop]['ph'] + avg[crop]['rainfall']) <= (avg[crop2]['N'] + avg[crop2]['P'] + avg[crop2]['K'] + avg[crop2]['temperature'] + avg[crop2]['humidity'] + avg[crop2]['ph'] + avg[crop2]['rainfall']) <= 1.1 * (avg[crop]['N'] + avg[crop]['P'] + avg[crop]['K'] + avg[crop]['temperature'] + avg[crop]['humidity'] + avg[crop]['ph'] + avg[crop]['rainfall']):
            similarity = abs(1 - (avg[crop2]['N'] + avg[crop2]['P'] + avg[crop2]['K'] + avg[crop2]['temperature'] + avg[crop2]['humidity'] + avg[crop2]['ph'] + avg[crop2]['rainfall']) / (avg[crop]['N'] + avg[crop]['P'] + avg[crop]['K'] + avg[crop]['temperature'] + avg[crop]['humidity'] + avg[crop]['ph'] + avg[crop]['rainfall']))
            similar_crops[crop].append((crop2, similarity))
                                        
# order the similar crops according to similarity
for crop in crops:
    similar_crops[crop] = sorted(similar_crops[crop], key=lambda x: x[1])

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
    seasons = ['Jan-Feb', 'Mar-May', 'Jun-Sep', 'Oct-Dec']
    month = datetime.datetime.now().month
    season = ''
    
    for i in range(0, len(seasons)):
        if month in range(i*3+1, i*3+4):
            season = seasons[i]
            break
        
    rainfall_data = pd.read_csv('rainfall/district_rainfall.csv')
    for i in range(0, len(rainfall_data)):
        if rainfall_data.iloc[i, 1] == district.upper():
            return rainfall_data.iloc[i, 14]
            
    return 100

def rainfall(i):
    seasons = ['Jan-Feb', 'Mar-May', 'Jun-Sep', 'Oct-Dec']
    rain_div = ['2', '3', '4', '3']
    
    return rain_div[i]

def getList(l):
    # convert elements of list to float
    for i in range(0, len(l)):
        for j in range(0, len(l[i])):
            l[i][j] = float(l[i][j])
        l[i][6] /= 12
    crops = model.predict(l)
    crop = crops[0]
    
    result = []
    result.append(crop)
    similar_crops_ = [x[0] for x in similar_crops[crop]]
    
    for k in similar_crops_:
        result.append(k)
    
    return result
    

def main(state, district):
    state = state.upper()
    
    (N, P, K) = getNPK(state)
    
    (temperature, humidity) = getWeather(district)
    
    ph = getPH(state)
    rainfall = getRainfall(district)
    
    predict_data = [[N, P, K, temperature, humidity, ph, rainfall]]
    return str(getList(predict_data))

@app.get('/')
def index(state, district):
    state = state.upper()
    
    (N, P, K) = getNPK(state)
    
    (temperature, humidity) = getWeather(district)
    
    ph = getPH(state)
    rainfall = getRainfall(district)
    
    predict_data = [[N, P, K, temperature, humidity, ph, rainfall]]
    return str(getList(predict_data))
    
