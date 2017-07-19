import ModeStandard, ModeSecure, sys

def usage():
	print('\n========================')
	print('OBD USAGE')
	print('========================\n')
	print('python3 run.py mode')
	print('        - mode: std or sec\n')
	exit()

if len(sys.argv) < 2: usage()
mode = sys.argv[1]
if mode == 'std':
	print('\nMode Standard')
	ModeStandard.main()
elif mode == 'sec':
	print('\nMode Secure')
	ModeSecure.main()
else: usage()
