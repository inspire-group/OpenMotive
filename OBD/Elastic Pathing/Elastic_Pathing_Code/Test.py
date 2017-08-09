# Import dependencies
from fastnumbers import float, fast_float
from random import shuffle
import matplotlib.pyplot as plt, numpy as np, os, re, sqlite3 as sql

# Open and store file
conn = sql.connect('track-5.sq3')
cur = conn.cursor()
cur.execute('SELECT * FROM speeds')
original = cur.fetchall()
original_speeds = [i[0] for i in original]

# Distance run by car
dist = float(os.popen('ruby elastic_pathing.rb \
./track-5.sq3 ./map.sq3').read().split(' ')[1])


def shuffle_round(skip_length=20, iterations=30, will_round=False, nearest=0):
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
			# and round if needed
			if will_round: new_speeds = [round(x, nearest) for x in original_speeds]
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
			result = fast_float(os.popen('ruby elastic_pathing.rb ./track-5.sq3 ./map.sq3').read().split(' ')[0], default=-1)
			if result >= 0: error += result
			else: no_results += 1
		threshold(new_speeds, thresh=20)
		errors[k] = 100*error/(iterations-no_results)/dist
	restore_file()
	if will_round: print('\nShuffling and rounding to %d\n' % int(10**(-nearest)))
	else: print('\nShuffling\n')
	for i in range(len(errors)): print('(%d, %f)' % (skips[i], errors[i]))

def round_only(nearest=0):
	# Make copy of original speed values and round
	new_speeds = [round(x, nearest) for x in original_speeds]
	threshold(new_speeds, thresh=20)
	# Save new values to file
	for j in range(len(original)):
		cur.execute('UPDATE speeds SET speed = %f WHERE time = %d' % (new_speeds[j], original[j][1]))
	conn.commit()
	# Run Elastic Pathing algorithm
	result = fast_float(os.popen('ruby elastic_pathing.rb ./track-5.sq3 ./map.sq3').read().split(' ')[0], default=-1)
	restore_file()
	print('\nRounding to %d\n' % int(10**(-nearest)))
	if result >= 0: print(result/dist)
	else: print('Error')

def restore_file():
	for entry in original: cur.execute('UPDATE speeds SET speed = %f WHERE time = %d' % (entry[0], entry[1]))
	conn.commit()

def threshold(speeds, thresh=0, with_time=False, original=False):
	count = 0
	if with_time:
		for entry in speeds:
			if entry[0] >= thresh: count += 1
	else:
		for entry in speeds:
			if entry >= thresh: count += 1
	if original: print('\nThreshold Original\n')
	else: print('\nThreshold\n')
	print('%d values above %f' % (count, thresh))

def plot(skips, errors):
	fit = np.polyfit(skips, errors, 1)
	fit_fn = np.poly1d(fit)
	plt.plot(skips, errors, skips, fit_fn(skips), '--r')
	plt.xlabel('Shuffling Interval (entries)')
	plt.ylabel('Relative Error (%)')
	plt.title('Relative Error vs. Shuffling Interval')
	plt.grid(True)
	plt.show()

try:
	round_only(nearest=0)
	print('\n' + ''.join(['=' for i in range(50)]))
	round_only(nearest=-1)
	print('\n' + ''.join(['=' for i in range(50)]))
	shuffle_round()
	print('\n' + ''.join(['=' for i in range(50)]))
	shuffle_round(will_round=True, nearest=0)
	print('\n' + ''.join(['=' for i in range(50)]))
	shuffle_round(will_round=True, nearest=-1)
except KeyboardInterrupt:
	restore_file()
	conn.close()
        exit()
