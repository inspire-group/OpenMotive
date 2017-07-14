import fileinput, json, os, sys

if len(sys.argv) < 5:
	print('\n========================')
	print('COUNT USAGE')
	print('========================\n')
	print('python3 count.py type PID threshold is_json')
	print('        - type: std or sec')
	print('        - PID:  PID hex value to filter')
	print('        - threshold: int <= values to be considered')
	print('        - is_json: True if log file already in json format\n')
	exit()

filename = 'log_' + str(sys.argv[1]) + '.txt'
pid = int(sys.argv[2], 16)
threshold = int(sys.argv[3])
is_json = str(sys.argv[4]) in ['true', 'TRUE', 'True', 'yes', 'YES', 'Yes', '1']

# Transform log file to json format
if not is_json:
	with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
		for line in file:
			if file.isfirstline(): line = line.replace('{', '[\n{')
			line = line.replace('{', '  {')
			print(line.replace('}', '},'), end='')
	with open(filename, 'rb+') as file:
		file.seek(-2, os.SEEK_END)
		file.truncate()
	with open(filename, 'a') as file:
		file.write('\n]')

# Read log as json file
with open(filename) as json_data:
	logs = json.load(json_data)
	count = 0
	for log in logs:
		if int(log['data'][2]) == pid:
			value = int(log['data'][3])
			if value >= threshold: count += 1
print(str(count) + ' values exceed the threshold')
