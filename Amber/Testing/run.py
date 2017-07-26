from Local import Local
from Cloud import Cloud
from Hybrid import Hybrid
import sys

def usage():
    print('\n========================')
    print('AMBER USAGE')
    print('========================\n')
    print('python3 run.py "mode" "plate1, plate2, plate3, ..."')
    print('        - mode: local or cloud or hybrid')
    exit()

if len(sys.argv) != 3: usage()

mode = sys.argv[1]
lps = sys.argv[2].upper().split(', ')

if mode not in ['local', 'cloud', 'hybrid']: usage()
alpr = None
if mode == 'local':
    alpr = Local()
    print('Local Mode')
elif mode == 'cloud':
    alpr = Cloud()
    print('Cloud Mode')
elif mode == 'hybrid':
    alpr = Hybrid()
    print('Hybrid Mode')
alpr.add(lps)
results = alpr.find()
for lp in results:
    print('\nFound vehicle ' + lp[0] + ', confidence = ' + lp[1])
