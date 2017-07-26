# Import dependencies
import cv2, json, os, skvideo.io, time

# Cloud mode plate detection
class Cloud(object):

    # Initialize Cloud Mode
    def __init__(self):
        self.FPS = 10
        self.lp = []
        time.sleep(0.1)

    # Add license plates to list
    def add(self, plates = []):
        self.lp.extend(plates)

    # Find license plates
    def find(self):
        plates_found = []
        metadata = skvideo.io.ffprobe('footage.mp4')['video']
        videodata = skvideo.io.vreader('footage.mp4',\
        num_frames = int(metadata['@nb_frames']))
        frame_rate = metadata['@avg_frame_rate'].split('/')
        skip_frames = int(round(int(frame_rate[0]) /\
        int(frame_rate[1]) / self.FPS))
        j = -1
        for frame in videodata:
            if cv2.waitKey(1) & 0xFF == ord("q"): break
            j += 1
            if j % skip_frames != 0: continue
            if not self.lp: break
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite("mode_cloud.jpg", img)
            results = json.loads(os.popen("curl -X POST -F \
            image0=@mode_cloud.jpg 'http://ec2-54-244-218-121.us-west-2.\
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
                        plates_found.append((candidate["plate"],\
                        str(candidate["confidence"])))
                        self.lp.remove(candidate["plate"])
        return plates_found
