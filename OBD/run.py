import sys

if len(sys.argv) < 2:
	print('\n========================')
	print('OBD USAGE')
	print('========================\n')
	print('python3 run.py mode')
	print('        - mode: std or sec\n')
	exit()
mode = sys.argv[1]
if mode == 'std':
	print('\nMode Standard')
	import ModeStandard
elif mode == 'sec':
	print('\nMode Secure')
	import ModeSecure
else:
	print('\n========================')
	print('OBD USAGE')
	print('========================\n')
	print('python3 run.py mode')
	print('        - mode: std or sec\n')
	exit()