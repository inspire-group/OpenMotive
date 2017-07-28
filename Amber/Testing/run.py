from Local import Local
from Cloud import Cloud
from Hybrid import Hybrid
import sys

def usage():
    print('\n========================')
    print('AMBER USAGE')
    print('========================\n')
    print('python3 run.py "mode" "fps" "resolution" "video_id" "plate1, plate2, plate3, ..."')
    print('        - mode: local or cloud or hybrid')
    print('        - fps: 1, 5, or 10')
    print('        - resolution: 720 or 1080')
    print('        - video_id: 1-6')
    exit()

if len(sys.argv) != 6: usage()

mode = sys.argv[1]
video_fps = sys.argv[2]
video_res = sys.argv[3]
video_id = sys.argv[4] 
lps = sys.argv[5].upper().split(', ')

if mode not in ['local', 'cloud', 'hybrid']\
or video_fps not in ['1', '5', '10']\
or video_res not in ['720', '1080']\
or video_id not in ['1', '2', '3', '4', '5', '6']: usage()
alpr = None
if mode == 'local':
    alpr = Local(fps=int(video_fps), res=int(video_res), vid_id=int(video_id))
    print('Local Mode')
elif mode == 'cloud':
    alpr = Cloud(fps=int(video_fps), res=int(video_res), vid_id=int(video_id))
    print('Cloud Mode')
elif mode == 'hybrid':
    alpr = Hybrid(fps=int(video_fps), res=int(video_res), vid_id=int(video_id))
    print('Hybrid Mode')
alpr.add(lps)
results = alpr.find()
for lp in results:
    print('\nFound vehicle ' + lp[0] + ', confidence = ' + lp[1])