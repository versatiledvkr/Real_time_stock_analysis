from flask import Flask, render_template, request, url_for
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import os
import numpy as np

if not os.path.exists('static'):
    os.makedirs('static')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    x = request.form['ticker']
    ts = TimeSeries(key='NUY8IH4PLHCREC1U', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=x, interval='1min', outputsize='full')
    close_data = data['4. close']
    y = np.arange(len(close_data))

    percentage_change = close_data.pct_change()
    End_pct = percentage_change[-1]
    if abs(End_pct) > 0.0004:
        result = x + ' ' + 'Alert sell' + str(End_pct)
    elif abs(End_pct) < 0.00075:
        result = x + ' ' + "Hold your Stock" + str(End_pct)
    elif abs(End_pct) < 0.000200:
        result = x + ' ' + "Buy the stock" + str(End_pct)
    else:
        result = "No action required"
    plot_url = plot_stock(close_data, y)
    return render_template('index.html', result=result, plot_url=plot_url)

def plot_stock(close_data, y):
    plt.figure(figsize=(10, 6))
    plt.plot(y, close_data)
    plt.xlabel('Trading Days')
    plt.ylabel('Stock Price')
    plt.title('Stock Data Analysis')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/plot.png')
    plot_url = url_for('static', filename='plot.png')
    return plot_url


if __name__ == '__main__':
    app.run(debug=True)

