from gps3 import agps3
from threading import Thread
import can, os, time

# Sampling rate (ms)
SAMPLING_RATE = 100

VEHICLE_SPEED = 0x0D
STEERING      = 0x80
PID_REQUEST   = 0x7DF
PID_REPLY     = 0x7E8

print('\nBringing up CAN0 (B)...')
os.system('sudo ip link set can0 up type can bitrate 500000')
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCan Board')
    exit()
print('Ready!\n')

RUN = True

can_queue = []

def read_can():
    while RUN:
        message = bus.recv()
        if message.arbitration_id == PID_REPLY:
            can_queue.insert(0, message)

def request_can():
    while RUN:
        message = can.Message(arbitration_id=PID_REQUEST, data=[0x02, 0x01,\
            VEHICLE_SPEED, 0x00, 0x00, 0x00, 0x00, 0x00], extended_id=False)
        bus.send(message)
        message = can.Message(arbitration_id=PID_REQUEST, data=[0x02, 0x01,\
            STEERING, 0x00, 0x00, 0x00, 0x00, 0x00], extended_id=False)
        bus.send(message)
    os.system('sudo ip link set can0 down')

gps_socket = agps3.GPSDSocket()
data_stream = agps3.DataStream()
gps_queue = []

def read_gps():
    gps_socket.connect()
    gps_socket.watch()
    for new_data in gps_socket:
        if not RUN: break
        if new_data:
            data_stream.unpack(new_data)
            gps_queue.insert(0, (data_stream.lat, data_stream.lon,\
                                 data_stream.time))

rx = Thread(target = read_can)
tx = Thread(target = request_can)
px = Thread(target = read_gps)

rx.start()
tx.start()
px.start()

start = time.time()
log = ''
try:
    while True:
        while (time.time() - start) % SAMPLING_RATE != 0: pass
        while not can_queue and not gps_queue: pass
        if len(can_queue) > 0:
            message = can_queue.pop()
            if message.arbitration_id == PID_REPLY and message.data[2]\
               == VEHICLE_SPEED:
                log += 'Speed: ' + str(int(message.data[3])) + ' Km/h, Time: '\
                       + str(message.timestamp) + '\n'
            if message.arbitration_id == PID_REPLY and message.data[2]\
               == STEERING:
                log += 'Steering: ' + str(int(message.data[3])) + ', ' +\
                    str(int(message.data[4])) + ', Time: '\
                    + str(message.timestamp) + '\n'
        if len(gps_queue) > 0:
            location = gps_queue.pop()
            log += 'Latitude: ' + location[0] + ', Longitude: '\
                   + location[1] + ', Time: ' + location[2] + '\n'
except KeyboardInterrupt:
    RUN = False
    with open('log.txt', 'a') as file:
        file.write(log)
