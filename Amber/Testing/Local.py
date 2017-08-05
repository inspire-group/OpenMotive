# Import dependencies
import cv2, json, os, skvideo.io, time

# Local mode plate detection
class Local(object):

    # Initialize Local Mode
    def __init__(self, fps=1, res=720):
        self.FPS = fps
        self.RES = res

    # Find license plate
    def find(self, lp=[]):
        start = time.time()
        metadata = skvideo.io.ffprobe('Footage/footage%d.mp4' % self.RES)['video']
        videodata = skvideo.io.vreader('Footage/footage%d.mp4' % self.RES)
        frame_rate = metadata['@avg_frame_rate'].split('/')
        skip_frames = int(round(int(frame_rate[0]) /\
        int(frame_rate[1]) / self.FPS))
        j = -1
        frames_count = 0
        for frame in videodata:
            if cv2.waitKey(1) & 0xFF == ord("q"): break
            if not lp: break
            j += 1
            if j % skip_frames != 0: continue
            frames_count += 1
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite("mode_local.jpg", img)
            results = json.loads(os.popen('alpr -j mode_local.jpg').read())
            i = 0
            for plate in results["results"]:
                i += 1
                for candidate in plate["candidates"]:
                    if candidate["plate"] in lp:
                        end = time.time()
                        lp.remove(candidate["plate"])
                        print('LOCAL - Plate %s, Latency %f, FPS %f, RES %d'\
                        % (candidate["plate"], (end-start)/frames_count,\
                        self.FPS, self.RES))
                        break
        print('\n\nDONE LOCAL\n\n')
