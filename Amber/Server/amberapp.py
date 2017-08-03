from flask import Flask, request
import json, os, time
app = Flask(__name__)

@app.route('/')
def index():
    return '<html><body><h1>AMBER Automatic License Plate Detection Service\
     - Princeton University</h1></body></html>\n'

@app.route('/alpr', methods = ['POST', 'GET'])
def detect():
    if request.method == 'POST':
        s = time.time()
        n = int(request.args.get('n', ''))
        mode = int(request.args.get('mode', ''))
        response = '['
        size = 0
        for i in range(0, n):
            img = request.files['image%d' % i]
            img.save('/home/ubuntu/amberapp/mode_cloud.jpg')
            size += int(os.stat('/home/ubuntu/amberapp/mode_cloud.jpg').st_size)
            response += os.popen('alpr -j \
            "/home/ubuntu/amberapp/mode_cloud.jpg"').read()
            if i != n - 1: response += ', '
        response += ']'
        e = time.time()
        f1 = open('/home/ubuntu/amberapp/time.txt', 'a')
        f1.write('%f\n' % (e - s))
        f1.close()
        if mode == 2: filename = 'sizeC'
        elif mode == 3: filename = 'sizeH'
        with open('/home/ubuntu/amberapp/%s.txt' % filename) as f2:
                lines = [x.strip() for x in f2.readlines()]
                if len(lines) > 0:
                        try: size += int(lines[0])
                        except: pass
        with open('/home/ubuntu/amberapp/%s.txt' % filename, 'w') as f2:
                f2.write(str(size))
        return response
    return '<html><body><h1>AMBER ALPR Upload Page</h1></body></html>\n'

if __name__ == '__main__':
    app.debug = True
    app.run()