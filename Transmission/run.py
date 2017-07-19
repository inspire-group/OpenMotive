import ModeSports, ModeEfficiency, sys

def usage():
    print('\n========================')
	print('Transmission USAGE')
	print('========================\n')
	print('python3 run.py mode type')
	print('        - mode: spo or eff\n')
    print('        - type: train or test')
	exit()

if len(sys.argv) < 3: usage()
mode = sys.argv[1]
phase = sys.argv[2]
if mode == 'spo' and phase == 'train':
    print('\nSports Mode - Training')
    ModeSports.main(mode='train')
elif mode == 'spo' and phase == 'test':
    print('\nSports Mode - Testing')
    ModeSports.main(mode='test')
elif mode == 'eff' and phase == 'train':
    print('\nEfficiency Mode - Training')
elif mode == 'eff' and phase == 'test':
    print('\nEfficiency Mode - Testing')
else: usage()
