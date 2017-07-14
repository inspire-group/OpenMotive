from flask import Flask, request
import json
app = Flask(__name__)

@app.route('/')
def index():
    return '<html><body><h1>OBDII Security and Privacy\
     Application - Princeton University</h1></body></html>'

@app.route('/log_std', methods = ['POST', 'GET'])
def log_std():
    if request.method == 'POST':
        f_std = open('/home/ubuntu/obdapp/log_std.txt', 'a')
        f_std.write(request.data + '\n')
        f_std.close()
        return '200STD'
    return '<html><body><h1>OBDII Standard Log Upload Page</h1></body></html>'

@app.route('/log_sec', methods = ['POST', 'GET'])
def log_sec():
    if request.method == 'POST':
        f_std = open('/home/ubuntu/obdapp/log_sec.txt', 'a')
        f_std.write(request.data + '\n')
        f_std.close()
        return '200SEC'
    return '<html><body><h1>OBDII Secure Log Upload Page</h1></body></html>'

if __name__ == '__main__':
    app.debug = True
    app.run()
