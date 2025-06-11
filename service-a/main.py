# # from flask import Flask
# # import requests, time, threading

# # app = Flask(__name__)

# # btc_prices = []

# # @app.route('/')
# # def home():
# #     return "Welcome to Service A! BTC price fetcher is running."

# # @app.route('/healthz')
# # def healthz():
# #     return 'OK', 200

# # @app.route('/ready')
# # def ready():
# #     return 'Ready', 200

# # def get_price():
# #     while True:
# #         try:
# #             response = requests.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json", verify=False)
# #             price = response.json()["bpi"]["USD"]["rate_float"]
# #             print(f"[{time.strftime('%H:%M:%S')}] BTC price: ${price}")
# #             btc_prices.append(price)
# #             if len(btc_prices) > 10:
# #                 btc_prices.pop(0)
# #             if len(btc_prices) == 10:
# #                 avg = sum(btc_prices) / 10
# #                 print(f"[{time.strftime('%H:%M:%S')}] 10-minute average: ${avg:.2f}")
# #         except Exception as e:
# #             print(f"Error fetching price: {e}")
# #         time.sleep(60)

# # if __name__ == '__main__':
# #     t = threading.Thread(target=get_price)
# #     t.daemon = True
# #     t.start()
# #     app.run(host='0.0.0.0', port=80)

# # if __name__ == "__main__":
# #     threading.Thread(target=get_price, daemon=True).start()

# #     app.run(host="0.0.0.0", port=80)







# from flask import Flask
# import requests, time, threading

# app = Flask(__name__)

# btc_prices = []

# @app.route('/')
# def home():
#     return "Welcome to Service A! BTC price fetcher is running."

# @app.route('/healthz')
# def healthz():
#     return 'OK', 200

# @app.route('/ready')
# def ready():
#     return 'Ready', 200

# def get_price():
#     while True:
#         try:
#             # CoinGecko API for Bitcoin price in USD
#             response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
#             response.raise_for_status()
#             price = response.json()["bitcoin"]["usd"]
#             print(f"[{time.strftime('%H:%M:%S')}] BTC price: ${price}")
#             btc_prices.append(price)
#             if len(btc_prices) > 10:
#                 btc_prices.pop(0)
#             if len(btc_prices) == 10:
#                 avg = sum(btc_prices) / 10
#                 print(f"[{time.strftime('%H:%M:%S')}] 10-minute average: ${avg:.2f}")
#         except Exception as e:
#             print(f"Error fetching price: {e}")
#         time.sleep(60)

# if __name__ == '__main__':
#     t = threading.Thread(target=get_price)
#     t.daemon = True
#     t.start()
#     app.run(host='0.0.0.0', port=80)





# from flask import Flask
# import requests, time, threading

# app = Flask(__name__)

# btc_prices = []

# @app.route('/')
# def home():
#     return "Welcome to Service A! BTC price fetcher is running."

# @app.route('/healthz')
# def healthz():
#     return 'OK', 200

# @app.route('/ready')
# def ready():
#     return 'Ready', 200

# def get_price():
#     while True:
#         try:
#             response = requests.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json", verify=False)
#             price = response.json()["bpi"]["USD"]["rate_float"]
#             print(f"[{time.strftime('%H:%M:%S')}] BTC price: ${price}")
#             btc_prices.append(price)
#             if len(btc_prices) > 10:
#                 btc_prices.pop(0)
#             if len(btc_prices) == 10:
#                 avg = sum(btc_prices) / 10
#                 print(f"[{time.strftime('%H:%M:%S')}] 10-minute average: ${avg:.2f}")
#         except Exception as e:
#             print(f"Error fetching price: {e}")
#         time.sleep(60)

# if __name__ == '__main__':
#     t = threading.Thread(target=get_price)
#     t.daemon = True
#     t.start()
#     app.run(host='0.0.0.0', port=80)

# if __name__ == "__main__":
#     threading.Thread(target=get_price, daemon=True).start()

#     app.run(host="0.0.0.0", port=80)








from flask import Flask
import requests, time, threading

app = Flask(__name__)

btc_prices = []
prices_lock = threading.Lock()  # כדי להגן על הגישה לרשימה בין התהליכים

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
        time.sleep(60)  # לחכות דקה לפני הפעם הבאה

def print_average():
    while True:
        time.sleep(600)  # לחכות 10 דקות
        with prices_lock:
            if len(btc_prices) == 10:
                avg = sum(btc_prices) / 10
                print(f"[{time.strftime('%H:%M:%S')}] 10-minute average: ${avg:.2f}")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Not enough data to calculate 10-minute average yet.")

if __name__ == '__main__':
    # thread לאיסוף מחירים
    t1 = threading.Thread(target=fetch_price, daemon=True)
    t1.start()

    # thread להדפסת ממוצע כל 10 דקות
    t2 = threading.Thread(target=print_average, daemon=True)
    t2.start()

    app.run(host='0.0.0.0', port=80)
