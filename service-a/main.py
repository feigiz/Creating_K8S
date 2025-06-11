from flask import Flask
import requests, time, threading

app = Flask(__name__)

btc_prices = []
prices_lock = threading.Lock()

@app.route('/')
def home():
    return "Welcome to Service A! BTC price fetcher is running."

@app.route('/healthz')
def healthz():
    return 'OK', 200

@app.route('/ready')
def ready():
    return 'Ready', 200

def fetch_price():
    while True:
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
            response.raise_for_status()
            price = response.json()["bitcoin"]["usd"]
            print(f"[{time.strftime('%H:%M:%S')}] BTC price: ${price}")
            with prices_lock:
                btc_prices.append(price)
                if len(btc_prices) > 10:
                    btc_prices.pop(0)
        except Exception as e:
            print(f"Error fetching price: {e}")
        time.sleep(60)

def print_average():
    while True:
        time.sleep(600)
        with prices_lock:
            if len(btc_prices) == 10:
                avg = sum(btc_prices) / 10
                print(f"[{time.strftime('%H:%M:%S')}] 10-minute average: ${avg:.2f}")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Not enough data to calculate 10-minute average yet.")

if __name__ == '__main__':
    t1 = threading.Thread(target=fetch_price, daemon=True)
    t1.start()

    t2 = threading.Thread(target=print_average, daemon=True)
    t2.start()

    app.run(host='0.0.0.0', port=80)
