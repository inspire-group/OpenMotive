# Import dependencies
import cv2, json, os, skvideo.io, time

# Cloud mode plate detection
class Cloud(object):

    # Initialize Cloud Mode
    def __init__(self, fps=1, res=720, vid_id=1, ip='0-0-0-0'):
        self.FPS = fps
        self.RES = res
        self.VID_ID = vid_id
        self.ip = ip

    # Find license plates
    def find(self, lp=''):
        start = time.time()
        metadata = skvideo.io.ffprobe('Footage/footage%d-%d.mp4' % (self.RES, self.VID_ID))['video']
        videodata = skvideo.io.vreader('Footage/footage%d-%d.mp4' % (self.RES, self.VID_ID),\
        num_frames = int(metadata['@nb_frames']))
        frame_rate = metadata['@avg_frame_rate'].split('/')
        skip_frames = int(round(int(frame_rate[0]) /\
        int(frame_rate[1]) / self.FPS))
        j = -1
        frames_count = 0
        for frame in videodata:
            if cv2.waitKey(1) & 0xFF == ord("q"): break
            j += 1
            if j % skip_frames != 0: continue
            frames_count += 1
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite("mode_cloud.jpg", img)
            results = json.loads(os.popen("curl -X POST -F \
            image0=@mode_cloud.jpg 'http://ec2-%s.us-west-2.\
            compute.amazonaws.com/alpr?n=1'" % self.ip).read())
            i = 0
            for plate in results[0]["results"]:
                i += 1
                for candidate in plate["candidates"]:
                    if candidate["plate"] == lp:
                        end = time.time()
                        return (end-start)/frames_count
        return -1
