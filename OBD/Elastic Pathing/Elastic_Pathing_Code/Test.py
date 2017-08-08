# Import dependencies
from fastnumbers import float, fast_float
from random import shuffle
import matplotlib.pyplot as plt, numpy as np, os, re, sqlite3 as sql

# Open and store file
conn = sql.connect('test-track.sq3')
cur = conn.cursor()
cur.execute('SELECT * FROM speeds')
original = cur.fetchall()
original_speeds = [i[0] for i in original]

# Number of entries to skip on each try
skips = [1]
for i in range(1, len(original)):
    if i % 20 == 0: skips.append(i)
skips.append(len(original))

# Number of iterations to run for each skip value
iterations = 30
# Number of tries/skips
num_skips = len(skips)
# Total number of elastic pathing runs
num_runs = num_skips*iterations
# Constant to convert completion to percentage
cst = 100/num_runs
# Distance run by car
dist = float(os.popen('ruby elastic_pathing.rb \
./test-track.sq3 ./map.sq3').read().split(' ')[1])

try:
    errors = [0.0] * num_skips
    # Get errors for shuffling with different intervals
    for k in range(num_skips):
        # Repeat to minimize randomness
        error = 0
        no_results = 0
        for i in range(iterations):
            # Set shuffle offset
            offset = 0
            # Make copy of original speed values
            new_speeds = original_speeds[:]
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
            result = fast_float(os.popen('ruby elastic_pathing.rb \
            ./test-track.sq3 ./map.sq3').read().split(' ')[0], default = -1)
            if result >= 0: error += result
            else: no_results += 1
            print('%f %%' % ((iterations*k + i + 1)*cst))
        errors[k] = 100*error/(iterations-no_results)/dist
    # Put back original values for reuse and close file
    for entry in original:
        cur.execute('UPDATE speeds SET speed = %f WHERE time = %d'\
        % (entry[0], entry[1]))
    conn.commit()
    print('File restored')
    # Plot results
    fit = np.polyfit(skips, errors, 1)
    fit_fn = np.poly1d(fit)
    plt.plot(skips, errors, skips, fit_fn(skips), '--r')
    plt.xlabel('Shuffling Interval (entries)')
    plt.ylabel('Relative Error (%)')
    plt.title('Relative Error vs. Shuffling Interval')
    plt.grid(True)
    plt.show()
except KeyboardInterrupt:
    conn.close()
    exit()
