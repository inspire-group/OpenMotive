# Import dependencies
from fastnumbers import float, fast_float
from random import shuffle
import matplotlib.pyplot as plt, numpy as np, os, random, re, sqlite3 as sql

# Track filename
file = 'track-5.sq3'

# Open and store file
conn = sql.connect(file)
cur = conn.cursor()
cur.execute('SELECT * FROM speeds')
original = cur.fetchall()
original_speeds = [i[0] for i in original]

# Distance travelled by car
dist = float(os.popen('ruby elastic_pathing.rb ./%s ./map.sq3' % file).read().split(' ')[1])


# Default threshold
DEF_THRESH = 20
# Default threshold exceeding number
ex_def_thresh = 0
for i in original_speeds:
	if i >= 20: ex_def_thresh += 1

# Run Elastic Pathing with shuffling (and rounding, and diff)
def shuffle_round_diff(skip_length=20, iterations=30, will_round=False, nearest=0, will_diff=False, diff_min=0, diff_max=10):
	skips = [1]
	for i in range(1, len(original)):
		if i % skip_length == 0: skips.append(i)
	skips.append(len(original))
	errors = [0.0] * len(skips)
	# Get errors for shuffling with different intervals
	for k in range(len(skips)):
		# Repeeat to minimize randomness
		error = 0
		no_results = 0
		for i in range(iterations):
			# Set shuffle offset
			offset = 0
			# Make copy of original speed values
			# and round/diff if needed
			if will_round and will_diff: print('Not Implemented')
			elif will_round: new_speeds = [round(x/nearest)*nearest for x in original_speeds]
			elif will_diff: new_speeds = [x + random.uniform(diff_min, diff_max) for x in original_speeds]
			else: new_speeds = original_speeds[:]
			# Shuffle values and save
			if skips[k] > 1:
				while offset < skips[-1]:
					end = offset + skips[k]
					if end > skips[-1]: end = skips[-1]
					shuffle_speeds = new_speeds[offset:end]
					shuffle(shuffle_speeds)
					new_speeds[offset:end] = shuffle_speeds
					offset += skips[k]
				for j in range(skips[-1]):
					cur.execute('UPDATE speeds SET speed = %f WHERE time = %d'\
					% (new_speeds[j], original[j][1]))
				conn.commit()
			# Run Elastic Pathing algorithm
			result = fast_float(os.popen('ruby elastic_pathing.rb ./%s ./map.sq3' % file).read().split(' ')[0], default=-1)
			if result >= 0: error += result
			else: no_results += 1
		threshold(new_speeds, thresh=DEF_THRESH)
		errors[k] = 100*error/(iterations-no_results)/dist
	restore_file()
	return (threshold(new_speeds, thresh=DEF_THRESH), [(skips[i], 100-errors[i]) for i in range(len(errors))])

def round_only(nearest=0):
	# Make copy of original speed values and round
	new_speeds = [round(x, nearest) for x in original_speeds]
	# Save new values to file
	for j in range(len(original)):
		cur.execute('UPDATE speeds SET speed = %f WHERE time = %d' % (new_speeds[j], original[j][1]))
	conn.commit()
	# Run Elastic Pathing algorithm
	result = fast_float(os.popen('ruby elastic_pathing.rb ./%s ./map.sq3' % file).read().split(' ')[0], default=-1)
	restore_file()
	return (int(10**(-nearest)), threshold(new_speeds, thresh=DEF_THRESH), 100*result/dist)

def restore_file():
	for entry in original: cur.execute('UPDATE speeds SET speed = %f WHERE time = %d' % (entry[0], entry[1]))
	conn.commit()

def threshold(speeds, thresh=0, with_time=False):
	count = 0
	if with_time:
		for entry in speeds:
			if entry[0] >= thresh: count += 1
	else:
		for entry in speeds:
			if entry >= thresh: count += 1
	return 100*abs(count-ex_def_thresh)/ex_def_thresh

def diff(min=0, max=10, iterations=30):
	average = 0
	error = 0
	no_results = 0
	for i in range(iterations):
		new_speeds = [x + random.uniform(min, max) for x in original_speeds]
		for j in range(len(original)): cur.execute('UPDATE speeds SET speed = %f WHERE time = %d' % (new_speeds[j], original[j][1]))
		conn.commit()
		result = fast_float(os.popen('ruby elastic_pathing.rb ./%s ./map.sq3' % file).read().split(' ')[0], default=-1)
		if result >= 0:
			average += result
			error += threshold(new_speeds, thresh=DEF_THRESH)
		else: no_results += 1
	average = 100 - (100*average/(dist*(iterations-no_results)))
	error /= iterations-no_results
	restore_file()
	return (error, average)

def plot(x, y):
	fit = np.polyfit(x, y, 1)
	fit_fn = np.poly1d(fit)
	plt.plot(x, y, x, fit_fn(x), '--r')
	plt.xlabel('Shuffling Interval (entries)')
	plt.ylabel('Relative Error (%)')
	plt.title('Relative Error vs. Shuffling Interval')
	plt.grid(True)
	plt.show()

try:
	print('\nDIFF ONLY from 0 to 10')
	print('(diff_max, (thresh_error, accuracy))')
	print('\n' + ''.join(['=' for i in range(50)]))
	print([(i, diff(0, i)) for i in range(11)])
	print('\n' + ''.join(['=' for i in range(50)]))
	print('\nSHUFFLE ONLY with resolution 20')
	print('(thresh_error, [(interval, accuracy)])')
	print('\n' + ''.join(['=' for i in range(50)]))
	print(shuffle_round_diff())
	print('\n' + ''.join(['=' for i in range(50)]))
	print('\nSHUFFLE with resolution 20 with ROUND 1')
	print('(thresh_error, [(interval, accuracy)])')
	print('\n' + ''.join(['=' for i in range(50)]))
	print(shuffle_round_diff(will_round=True, nearest=1))
	print('\n' + ''.join(['=' for i in range(50)]))
	print('\nSHUFFLE with resolution 20 with ROUND 5')
	print('(thresh_error, [(interval, accuracy)])')
	print('\n' + ''.join(['=' for i in range(50)]))
	print(shuffle_round_diff(will_round=True, nearest=5))
	print('\n' + ''.join(['=' for i in range(50)]))
	print('\nSHUFFLE with resolution 20 with ROUND 10')
        print('(thresh_error, [(interval, accuracy)])')
        print('\n' + ''.join(['=' for i in range(50)]))
        print(shuffle_round_diff(will_round=True, nearest=10))
        print('\n' + ''.join(['=' for i in range(50)]))
	for j in [2, 4, 6, 8, 10]:
		print('\nSHUFFLE with resolution 20 with DIFF %d' % j)
	        print('(thresh_error, [(interval, accuracy)])')
        	print('\n' + ''.join(['=' for i in range(50)]))
	        print(shuffle_round_diff(will_diff, diff_max=j))
        	print('\n' + ''.join(['=' for i in range(50)]))
except KeyboardInterrupt:
	restore_file()
	conn.close()
        exit()
