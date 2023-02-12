# TRINIT_594092-U907K6ON_ML
The initial model uses the lightgbm library to train a model on the data. It is a gradient boosting model that uses decision trees as the base learners and provides a fast and accurate way to train a model. The model is 'Crop_recommendation.csv' data.

# Technical Stack
- Django for backend
- HTML, CSS, Bootstrap for frontend
- LightGBM for model training

# How to run the project

## To run the API
- Clone the repository
- Install the requirements using `pip install -r requirements.txt`
- Run the server using `python -m uvicorn main:app --reload`

## To run the web application
- Clone the repository
- Create a virtual environment if you want to by using `python -m venv env`
- Activate the virtual environment using `env\Scripts\activate`
- Install the requirements using `pip install -r requirements.txt`
- Run the server using `python crop_prediction/manage.py runserver`

# Deployment
The project can be temporarily deployed by using ngrok. To do so, run the following command in the terminal:
`ngrok http 8000`

Drive link:
https://drive.google.com/drive/folders/17npMQ3NCsr9rKHrdKSriSMQHBSucil73?usp=sharing
