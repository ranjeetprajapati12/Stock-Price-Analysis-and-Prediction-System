from flask import Flask, render_template, request, jsonify
import base64
import plotly.io as pio
import base64
import yfinance as yf
from datetime import timedelta,date
import io
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
from src.utils import additional_info
from sklearn.model_selection import train_test_split
#Import The libraries required for the deep learning algorith
#from tensorflow import keras 
from keras import models
from keras import layers
#from keras import Dense ,LSTM
from sklearn.metrics import r2_score
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/predict')
def predict():
    return render_template("predict.html")

@app.route('/service')
def service():
    return render_template("service.html")

@app.route('/team')
def team():
    return render_template("abc.html")

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    data = request.json
    symbol = data.get('symbol', 'AAPL') 
    # Set the date range
    today=date.today()
    d1 = today.strftime("%Y-%m-%d")
    end_date= d1
    d2=date.today()-timedelta(days=500)
    start_date = d2.strftime("%Y-%m-%d")
    
    end_date = end_date

    # Download the data
    try:
        print("running this")
        data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to get data, Please Check the Ticker, It must be a valid name"}), 500

    data["Date"] = data.index
    data = data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    data.set_index("Date", inplace=True)

    # Plotting the candlestick chart
     # Generate the plot
    plt.ioff()
    buffer = io.BytesIO()
    try:
        mpf.plot(data, type='candle', style='charles',
                 title=f"{symbol} Stock Price Analysis",
                 ylabel='Price ($)', volume=True,
                 savefig=dict(fname=buffer, format='png'))
    except Exception as e:
        print("Error plotting data:", e)
        return jsonify({"error": "Failed to generate plot"}), 500
    
    buffer.seek(0)
    plot_url = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    info = additional_info(symbol=symbol)
    return jsonify({'plot_url': plot_url,"info":info})

@app.route('/predict', methods=['POST'])
def predicts():
    data = request.json
    symbol = data.get('symbol', 'AAPL') 
    # Set the date range
    today=date.today()
    d1 = today.strftime("%Y-%m-%d")
    end_date= d1
    d2=date.today()-timedelta(days=500)
    start_date = d2.strftime("%Y-%m-%d")
    print("asdsadasdsas")
    end_date = end_date

    # Download the data
    try:
        print("running this")
        data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to get data, Please Check the Ticker, It must be a valid name"}), 500

    data["Date"] = data.index
    data = data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    data.set_index("Date", inplace=True)
    y=data.iloc[:,4]
    x=data.loc[:,["Open","High","Low","Adj Close","Volume"]]

    #Train and test data separation
    xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=.3,random_state=13)

    # creating the model
    model=models.Sequential()

    #adding the different Layer(Nodes) arguements to model
    model.add(layers.LSTM(128, return_sequences=True, input_shape= (xtrain.shape[1], 1)))

    #adding second neural network layer with 64 Nodes
    model.add(layers.LSTM(64, return_sequences=False))

    #adding 3rd layer
    model.add(layers.Dense(25))

    #adding output layer
    model.add(layers.Dense(1))

    # Let's Train the model now
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(xtrain, ytrain, batch_size=1, epochs=30)

    # predict the close for test data
    pred=model.predict(xtest)

    accuracy=r2_score(ytest,pred)
    print("Accuracyis:",accuracy)

    today=date.today()
    d1 = today.strftime("%Y-%m-%d")
    end_date= d1
    d2=date.today()-timedelta(days=1)
    start_date=d2.strftime("%Y-%m-%d")
    data=yf.download("GOOG",start=start_date,end=end_date,progress=False)

    z=[[data["Open"].values[0],data["High"].values[0],data["Low"].values[0],data["Adj Close"].values[0]]]
    features = np.array(z)
    print("Prediction is:",model.predict(features)[0][0])
    # Plotting the candlestick chart
     # Generate the plot
    # plt.ioff()
    # buffer = io.BytesIO()
    # try:
    #     mpf.plot(data, type='candle', style='charles',
    #              title=f"{symbol} Stock Price Analysis",
    #              ylabel='Price ($)', volume=True,
    #              savefig=dict(fname=buffer, format='png'))
    # except Exception as e:
    #     print("Error plotting data:", e)
    #     return jsonify({"error": "Failed to generate plot"}), 500
    
    # buffer.seek(0)
    # plot_url = base64.b64encode(buffer.getvalue()).decode('utf-8')
    # buffer.close()
    # plt.close()
    info = additional_info(symbol=symbol)
    return jsonify({"info":info})

if __name__ == '__main__':
    app.run(debug=True)
