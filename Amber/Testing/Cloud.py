# Import dependencies
import cv2, json, os, skvideo.io, time

# Cloud mode plate detection
class Cloud(object):

    # Initialize Cloud Mode
    def __init__(self, fps=1, res=720, vid_id=1):
        self.FPS = fps
        self.RES = res
        self.VID_ID = vid_id
        self.lp = []
        time.sleep(0.1)

    # Add license plates to list
    def add(self, plates = []):
        self.lp.extend(plates)

    # Find license plates
    def find(self):
        start = time.time()
        plates_found = []
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
            if not self.lp: break
            j += 1
            if j % skip_frames != 0: continue
            frames_count += 1
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite("mode_cloud.jpg", img)
            results = json.loads(os.popen("curl -X POST -F \
            image0=@mode_cloud.jpg 'http://ec2-34-211-111-163.us-west-2.\
            compute.amazonaws.com/alpr?n=1'").read())
            i = 0
            for plate in results[0]["results"]:
                i += 1
                print("\nPlate #%d" % i)
                print("   %12s %12s" % ("Plate", "Confidence"))
                for candidate in plate["candidates"]:
                    prefix = "-"
                    if candidate["matches_template"]:
                        prefix = "*"
                    print("   %s %12s%12f" % (prefix,\
                    candidate["plate"], candidate["confidence"]))
                    if candidate["plate"] in self.lp:
                        end = time.time()
                        plates_found.append((candidate["plate"],\
                        str(candidate["confidence"])))
                        self.lp.remove(candidate["plate"])
                        print('\nLatency ratio: %f, FPS: %d' % ((end-start)/frames_count, self.FPS))
        return plates_found
