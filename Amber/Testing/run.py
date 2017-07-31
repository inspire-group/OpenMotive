from Local import Local
from Cloud import Cloud
from Hybrid import Hybrid
import sys

PLATES = [1:'78197', 2:'T638802C', 3:'T640951C', 4:'N49EPU', 5:'382946', 6:'R43HBY',\
          7:'X35ELG', 8:'V68EPT', 9:'JCG92V', 10:'EEB4657', 11:'5N23', 12:'GDB3917']

def usage():
    print('\n========================')
    print('AMBER USAGE')
    print('========================\n')
    print('python3 run.py "mode" "ip" "perf"')
    print('        - mode: local or cloud or hybrid')
    print('        - ip: AWS ip (e.g. 0.0.0.0) - required in Cloud and Hybrid modes\n')
    print('        - perf: performance testing - sets FPS and Resolution to max')
    exit()

PERF = False
if len(sys.argv) < 2: usage()
mode = sys.argv[1]
if mode not in ['local', 'cloud', 'hybrid']: usage()
if len(sys.argv) == 2:
    if mode != 'local': usage()
elif len(sys.argv) == 3:
    if sys.argv[2] == 'perf':
        if mode != 'local': usage()
        PERF = True
    else: aws_ip = '-'.join(sys.argv[2].split('.'))
elif len(sys.argv) == 4:
    if sys.argv[3] == 'perf': PERF = True
    else: usage()
    aws_ip = '-'.join(sys.argv[2].split('.'))
else: usage()

FPS = 10
RES = 1080
alpr = None
for video_id in range(1, 13):
    if PERF:
        if mode == 'local': alpr = Local(fps=FPS, res=RES, vid_id=video_id)
        elif mode == 'cloud': alpr = Cloud(fps=FPS, res=RES, vid_id=video_id, ip=aws_ip)
        elif mode == 'hybrid': alpr = Hybrid(fps=FPS, res=RES, vid_id=video_id, ip=aws_ip)
        print("PERFORMANCE - SPAF: %f" % alpr.find(PLATES[video_id]))
    else:
        for video_fps in [1, 5, 10]:
            if mode == 'local': alpr = Local(fps=video_fps, res=RES, vid_id=video_id)
            elif mode == 'cloud': alpr = Cloud(fps=video_fps, res=RES, vid_id=video_id, ip=aws_ip)
            elif mode == 'hybrid': alpr = Hybrid(fps=video_fps, res=RES, vid_id=video_id, ip=aws_ip)
            print("FPS %d - SPAF: %f" % (video_fps, alpr.find(PLATES[video_id])))
        for video_res in [720, 1080]:
            if mode == 'local': alpr = Local(fps=FPS, res=video_res, vid_id=video_id)
            elif mode == 'cloud': alpr = Cloud(fps=FPS, res=video_res, vid_id=video_id, ip=aws_ip)
            elif mode == 'hybrid': alpr = Hybrid(fps=FPS, res=video_res, vid_id=video_id, ip=aws_ip)
            print("RES %d - SPAF: %f" % (video_res, alpr.find(PLATES[video_id])))
