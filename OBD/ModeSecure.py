# Import dependencies
from random import shuffle
from threading import Thread
import can, os, queue, requests, time

# PIDs for OBDII
PID_REQUEST = 0x7DF
PID_REPLY = 0x7E8

# Keep threads running
RUN = True
# Time until send responses in random order (sec)
RESPONSE_INTERVAL = 60

print('\nReading requests from CAN1, transmitting them to CAN0,')
print('and returning them to CAN1, without any data modification...')

# Bring up CAN0 (B) and CAN1 (A) interface at 500kbps
os.system('sudo ip link set can0 up type can bitrate 500000')
os.system('sudo ip link set can1 up type can bitrate 500000')
time.sleep(0.1)
print('Ready\n')

try:
    bus0 = can.interface.Bus(channel='can0', bustype='socketcan_native')
    bus1 = can.interface.Bus(channel='can1', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board')
    exit()

# Receive requests from CAN1
def rx_can1():
    while RUN:
        request = bus1.recv()
        if request.arbitration_id == PID_REQUEST:
            requestQ.put(request)
    os.system('sudo ip link set can1 down')

# Transmit request to CAN0
def tx_can0(message_data = [0x02, 0x01, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00]):
    msg = can.Message(arbitration_id=PID_REQUEST, data=message_data,\
    extended_id=False)
    bus0.send(msg)
    time.sleep(0.05)

# Receive response from CAN0
def rx_can0():
    while RUN:
        response = bus0.recv()
        if response.arbitration_id == PID_REPLY:
            responseQ.put(response)
            message = {'data':response.data, 'timestamp':response.timestamp}
            requests.post('http://ec2-54-190-35-163.us-west-2\
            .compute.amazonaws.com/log_sec', json=message)
    os.system('sudo ip link set can0 down')

# Transmit response to CAN1
def tx_can1(message_data = [0x02, 0x01, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00]):
    msg = can.Message(arbitration_id=PID_REPLY, data=message_data,\
    extended_id=False)
    bus1.send(msg)
    time.sleep(0.05)

# Manipulate data to stop information leakage
def secure(data):
    return shuffle(data)

# Start receiving requests and responses
# on different threads
requestQ = queue.Queue()
responseQ = queue.Queue()
rx0 = Thread(target=rx_can0)
rx1 = Thread(target=rx_can1)
rx0.start()
rx1.start()

# Read from CAN1, request from CAN0,
# then read from CAN0, transmit to CAN1
try:
    start = time.time()
    while True:
        if not requestQ.empty():
            request = requestQ.get()
            tx_can0(request.data)
        if (time.time() - start) % RESPONSE_INTERVAL == 0:
            responses = []
            while not responseQ.empty(): responses.append(responseQ.get())
            for response in secure(responses): tx_can1(response.data)
except KeyboardInterrupt: RUN = False
