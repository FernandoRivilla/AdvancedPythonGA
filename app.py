from flask import Flask, request
from ie_bike_model import ai
import ie_bike_model
import sys
import time
import sklearn


app = Flask(__name__)

@app.route('/')
def hello():

    return {"Scikit version:":sklearn.__version__, "Python version:":'.'.join(map(str,sys.version_info)), "ie_bike_model":ie_bike_model.__version__}


@app.route('/predict')
def predict():
    start_time = time.time()

    dteday = request.args.get('dteday')
    hr = int(request.args.get('hr'))
    weathersit = request.args.get('weathersit')
    temp = float(request.args.get('temp'))
    atemp = float(request.args.get('atemp'))
    hum = float(request.args.get('hum'))
    windspeed = float(request.args.get('windspeed'))
    result = ai.predict(dteday=dteday,
    hr=hr, 
    weathersit=weathersit,
    temp=temp,
    atemp=atemp,
    hum=hum,
    windspeed=windspeed)
    return {"result": result, "elapsed_fime": (time.time() - start_time)}

@app.route('/train_and_persist')
def train_and_persist():
    ai.train_and_persist()
    return {"status": "ok"}

app.run(host="0.0.0.0",port=sys.argv[1])