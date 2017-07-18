# Import dependencies
from random import shuffle
import matplotlib.pyplot as plt, os, re, sqlite3 as sql

# Number of entries to skip on each try
skips = [1]
for i in range(1, 528):
    if i % 10 == 0: skips.append(i)

# Open and store file
conn = sql.connect('test-track.sq3')
cur = conn.cursor()
cur.execute('SELECT * FROM speeds')
original_speeds = cur.fetchall()

try:
    errors = []
    # Get errors for shuffling with different intervals
    for skip in skips:
        # Repeat to minimize randomness
        error = 0
        no_results = 0
        iterations = 20
        for i in range(iterations):
            # Set shuffle offset
            offset = 0
            # Make copy of original values
            new_speeds = original_speeds[:]
            # Shuffle values and save
            if skip > 1:
                while offset < len(new_speeds):
                    end = offset + skip
                    if end > len(new_speeds): end = len(new_speeds)
                    shuffle_speeds = new_speeds[offset:end]
                    shuffle(shuffle_speeds)
                    new_speeds[offset:end] = shuffle_speeds
                    offset += skip
                for j in range(0, len(new_speeds)):
                    cur.execute('UPDATE speeds SET speed = ' \
                    + str(new_speeds[j][0]) + ' WHERE time = '\
                    + str(original_speeds[j][1]))
            conn.commit()
            print('Iteration %d, Skip %d' % (i, skip))
            # Run Elastic Pathing algorithm
            result = os.popen('ruby elastic_pathing.rb \
            ./test-track.sq3 ./map.sq3').read()
            a = re.search(r'Dist is [0-9]+\.[0-9]+ miles', result)
            if a: error += float(result[a.start()+8:a.end()-6])
            else: no_results += 1
        errors.append(error/(iterations-no_results))
    # Plot results
    plt.plot(skips, errors)
    plt.xlabel('Shuffling Interval (entries)')
    plt.ylabel('Endpoint Error (miles)')
    plt.title('Endpoint Error vs. Shuffling Interval')
    plt.grid(True)
    plt.show()
except KeyboardInterrupt:
    # Put back original values for reuse and close file
    print('Restoring file...')
    for entry in original_speeds:
        cur.execute('UPDATE speeds SET speed = ' \
        + str(entry[0]) + ' WHERE time = '\
        + str(entry[1]))
    conn.commit()
    print('File restored')
    conn.close()
    exit()
