from flask import Flask, jsonify
from flask_cors import CORS
from alpaca_trade_api.rest import REST, TimeFrame

app = Flask(__name__)
CORS(app)

# Alpaca API credentials

API_KEY = "PKLCVJU4KFGW6P7JO2BW"
API_SECRET = "WvpwMXCyAhV3NjncwihgSldhpaXU4HdYEDozFeUI"
BASE_URL = "https://paper-api.alpaca.markets"

alpaca = REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

@app.route('/api/account', methods=['GET'])
def get_account():
    account = alpaca.get_account()
    return jsonify({
        'cash': account.cash,
        'buying_power': account.buying_power,
        'status': account.status,
    })

@app.route('/api/positions', methods=['GET'])
def get_positions():
    positions = alpaca.list_positions()
    positions_data = [{'symbol': pos.symbol, 'qty': pos.qty, 'market_price': pos.current_price, 'cost_basis': pos.cost_basis} for pos in positions]
    return jsonify(positions_data)

@app.route('/api/historical-data/<symbol>', methods=['GET'])
def get_historical_data(symbol):
    try:
        barset = alpaca.get_barset(symbol, TimeFrame.Day, limit=100)  # Get last 100 days
        data = [{'time': str(bar.t), 'close': bar.c} for bar in barset[symbol]]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002, debug=True)
