# Import dependencies
from threading import Thread
import can, numpy as np, os, requests, time

# Golden Ratio
PHI = (math.sqrt(5)+1)/2

# PIDs for OBDII
PID_REQUEST = 0x7DF
PID_REPLY = 0x7E8
# Mode 01
ENGINE_RPM = 0x0C
VEHICLE_SPEED = 0x0D
# Mode 09
PID_VIN = 0x02

# Keep threads running
RUN = True

# Bring up CAN0 (B) interface at 500kbps
os.system('sudo ip link set can0 up type can bitrate 500000')
time.sleep(0.1)
print('Ready\n')

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board')
    exit()

# !!! No need for 5th gear values since there is no switch to 6th gear !!!
# Map from RPM value to acceleration for all 4 gears
rpm2acc = {1:{}, 2:{}, 3:{}, 4:{}}
# Map from gear to optimal RPM interval discovered
gear2rpm = {1:[0, 5000], 2:[0, 5000], 3:[0, 5000], 4:[0, 5000]}
# Map from gear to final and optimal RPM
gear_optimal = {1:-1, 2:-1, 3:-1, 4:-1}
# Store current gear
gear = 1
# Store Vehicle Identification Number
VIN = -1

# RPM values precision
RPM_PRECISION = 100
# Round RPM to nearest acceptable value
def round_rpm(rpm):
    return int(round(rpm*RPM_PRECISION)/RPM_PRECISION)

# Get acceleration from two speed values
def acc(value1, value2):
    return (value2[0] - value1[0])/(value2[1] - value1[1])

# Get average acceleration from multiple speed values
def acc_avg(val):
    return np.mean([acc(val[i-1], val[i]) for i in range(1, len(val))])

# Get Vehicle Identification Number
def vin():
    msg = can.Message(arbitraion_id=PID_REQUEST, data=[0x02, 0x09, PID_VIN,\
    0x00, 0x00, 0x00, 0x00, 0x00], extended_id=False)
    bus.send(msg)
    time.sleep(0.05)
    while True:
        request = bus.recv()
        if request.arbitration_id == PID_REPLY and int(request.data[1]) == 0x09\
        and int(request.data[2], 16) == 0x02: return request.data[3:]

# Get Engine RPM and speed values from Vehicle
def get_values():
    os.popen('candump can0 > can_log.txt')
    while RUN:
        with open('can_log.txt', 'rw+') as f:
            for line in f:
                processLine(line)
            f.truncate(0)
    os.system('sudo ip link set can0 down')

# Ask user to drive at specific RPM
def ask(rpm):
    if not rpm in rpm2acc[gear]:
        print('Please switch to gear %d at %d RPM', (gear+1, rpm))
        while not rpm in rpm2acc[gear]: pass
    return rpm

# Golden Section Search algorithm
def gss():
    if gear_optimal[gear] != -1:
        c = ask(round_rpm(gear2rpm[gear][1]-(gear2rpm[gear][1]\
        -gear2rpm[gear][0])/PHI))
        d = ask(round_rpm(gear2rpm[gear][0]+(gear2rpm[gear][1]\
        -gear2rpm[gear][0])/PHI))
        if abs(c-d) > RPM_PRECISION:
            if rpm2acc[gear][c] > rpm2acc[gear][d]:
                gear2rpm[gear][1] = d
            else:
                gear2rpm[gear][0] = c

# Check if optimal RPM found for every gear
def done():
    for i in gear_optimal.values():
        if i == -1: return False
    return True

# Upload optimal RPMs found to the cloud
def upload():
    data = {'vin':VIN, 'rpm':gear_optimal}
    requests.post('ec2-34-211-111-136.us-west-2.compute.amazonaws.com/spo',\
    json=data)

# Download optimal RPMs found on the cloud
def download_optimal():
    data = {'vin':VIN}
    r = requests.get('ec2-34-211-111-136.us-west-2.compute.amazonaws.com/spo',\
    params=data)
    return json.loads(r.json())

# Run script
def main(mode='train'):
    # Read VIN
    VIN = vin()
    print('VIN: ' + VIN)
    # Start sniffing all values from car
    sniff = Thread(target=get_values)
    sniff.start()
    try:
        if mode == 'train':
            # Find optimal RPM for each gear
            while not done(): gss()
            print('\nOptimal Values found (Gear:RPM)')
            print(gear_optimal)
            upload()
        elif mode == 'test':
            next_gear = gear + 1
            opt = download_optimal()
            while True:
                if next_gear < 6 and next_gear != gear:
                    print('Change to gear %d at %d RPM',\
                    % (next_gear, opt[gear]))
                while next_gear != gear or gear == 5: pass
                next_gear = gear + 1
    except KeyboardInterrupt: RUN = False

if __name__ == '__main__': main()
