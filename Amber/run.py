from ModeRaspi import ModeRaspi
from ModeCloud import ModeCloud
from ModeBoth import ModeBoth
import sys

def usage():
    print('\n========================')
    print('AMBER USAGE')
    print('========================\n')
    print('python3 run.py "mode" "cam_option" "plate1, plate2, plate3, ..."')
    print('        - mode: raspi or cloud or both')
    print('        - cam_option: cam (camera) or ftg (footage)')
    exit()

if len(sys.argv) != 4: usage()

mode = sys.argv[1]
cam = sys.argv[2]
lps = sys.argv[3].upper().split(', ')

if mode not in ['raspi', 'cloud', 'both'] or cam not in ['cam', 'ftg']: usage()
alpr = None
if mode == 'raspi':
    alpr = ModeRaspi(footage = (cam == 'ftg'))
    print('Raspberry Pi Mode')
elif mode == 'cloud':
    alpr = ModeCloud(footage = (cam == 'ftg'))
    print('Cloud Mode')
elif mode == 'both':
    alpr = ModeBoth(footage = (cam == 'ftg'))
    print('Both Mode')
alpr.add(lps)
results = alpr.find()
for lp in results:
    print('\nFound vehicle ' + lp[0] + ', confidence = ' + lp[1])
