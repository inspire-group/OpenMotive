from Local import Local
from Cloud import Cloud
from Hybrid import Hybrid
import sys

PLATES = ['9D41', '1Y31', 'E23GLV', 'OL4958J', 'AP118Y', 'T687892C',\
            '1K59', '8J39', 'ROAD70', 'T635970C', 'T666363C', '5L95'\
            'EEK5870', '4M38']

def usage():
    print('\n========================')
    print('AMBER USAGE')
    print('========================\n')
    print('python3 run.py "mode" "ip" "perf"')
    print('        - mode: local, cloud or hybrid')
    print('        - ip: AWS ip (e.g. 0.0.0.0) - required in Cloud and Hybrid modes')
    print('              (keep empty if not needed)')
    print('        - perf: performance testing - sets FPS and Resolution to max')
    print('                (keep empty if not needed)\n')
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
if PERF:
    FPS = 1
    RES = 720
    if mode == 'local': alpr = Local(fps=FPS, res=RES)
    elif mode == 'cloud': alpr = Cloud(fps=FPS, res=RES, ip=aws_ip)
    elif mode == 'hybrid': alpr = Hybrid(fps=FPS, res=RES, ip=aws_ip)
    print('\n\nPERFORMANCE\n\n')
    COPY = PLATES[:]
    alpr.find(COPY)
    print('\n\nDONE PERFORMACE\n\n')
else:
#    for video_fps in [1, 5, 10]:
    for video_fps in [0.1, 0.5]:
        if mode == 'local': alpr = Local(fps=video_fps, res=RES)
        elif mode == 'cloud': alpr = Cloud(fps=video_fps, res=RES, ip=aws_ip)
        elif mode == 'hybrid': alpr = Hybrid(fps=video_fps, res=RES, ip=aws_ip)
        print('\n\n%d FPS\n\n' % video_fps)
        COPY = PLATES[:]
        alpr.find(COPY)
        print('\n\nDONE FPS\n\n')
#    for video_res in [720, 1080]:
#        if mode == 'local': alpr = Local(fps=FPS, res=video_res)
#        elif mode == 'cloud': alpr = Cloud(fps=FPS, res=video_res, ip=aws_ip)
#        elif mode == 'hybrid': alpr = Hybrid(fps=FPS, res=video_res, ip=aws_ip)
#        print('\n\n%d RESOLUTION\n\n' % video_res)
#        COPY = PLATES[:]
#        alpr.find(COPY)
#        print('\n\nDONE RESOLUTION\n\n')
