from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Service B!"

@app.route('/healthz')
def healthz():
    return 'OK', 200

@app.route('/ready')
def ready():
    return 'Ready', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
