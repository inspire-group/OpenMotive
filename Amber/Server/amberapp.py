from flask import Flask, request
import json, os, time
app = Flask(__name__)

@app.route('/')
def index():
    return '<html><body><h1>AMBER Automatic License Plate Detection Service\
     - Princeton University</h1></body></html>'

@app.route('/alpr', methods = ['POST', 'GET'])
def detect():
    if request.method == 'POST':
        s = time.time()
        n = int(request.args.get('n', ''))
        response = '['
        for i in range(0, n):
            img = request.files['image%d' % i]
            img.save('/home/ubuntu/amberapp/mode_cloud.jpg')
            response += os.popen('alpr -j \
            "/home/ubuntu/amberapp/mode_cloud.jpg"').read()
            if i != n - 1: response += ', '
        response += ']'
        e = time.time()
        f1 = open('/home/ubuntu/amberapp/time.txt', 'a')
        f1.write('%f\n' % (e - s))
        f1.close()
        with open('/home/ubuntu/amberapp/size.txt', 'wr+') as f2:
            f2.writelines(int(lines[0]) + int(os.stat('/home/ubuntu/amberapp/mode_cloud.jpg').st_size))
        return response
    return '<html><body><h1>AMBER ALPR Upload Page</h1></body></html>'

if __name__ == '__main__':
    app.debug = True
    app.run()
