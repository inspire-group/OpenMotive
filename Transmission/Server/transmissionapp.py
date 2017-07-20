from flask import Flask, request
import json
app = Flask(__name__)

@app.route('/')
def index():
    return '<html><body><h1>Vehicle Transmission Sports and Efficiency\
     Application - Princeton University</h1></body></html>'

@app.route('/spo', methods = ['POST', 'GET'])
def sports():
    if request.method == 'POST':
        return '200SPOP'
    if request.method == 'GET':
        return '200SPOG'
    return '<html><body><h1>Transmission Sports Upload Page</h1></body></html>'

@app.route('/eff', methods = ['POST', 'GET'])
def efficiency():
    if request.method == 'POST':
        return '200EFFP'
    if request.method == 'GET':
        return '200EFFG'
    return '<html><body><h1>Transmission Efficiency\
     Upload Page</h1></body></html>'

if __name__ == '__main__':
    app.debug = True
    app.run()
