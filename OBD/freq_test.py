import can, os, time

print('\nBringing up CAN0 (B)...')
os.system('sudo ip link set can0 up type can bitrate 500000')
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCan Board')
    exit()
print('Ready!\n')

try:
    count = 0
    start = time.time()
    while True:
        message = bus.recv()
        print(message)
        if message.arbitration_id == PID_REQUEST:
            count += 1
except KeyboardInterrupt:
    end = time.time()
    print('Frequency: %f' % (float(count)/float(end-start)))
    os.system('sudo ip link set can0 down')
