import sys

def usage():
    print('\n========================')
	print('Transmission USAGE')
	print('========================\n')
	print('python3 run.py mode')
	print('        - mode: spo or eff\n')
	exit()

if len(sys.argv) < 2: usage()
mode = sys.argv[1]
if mode == 'spo':
	print('\nMode Sports')
	import ModeSports
elif mode == 'eff':
	print('\nMode Efficiency')
	import ModeEfficiency
else: usage()
