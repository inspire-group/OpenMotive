# Import dependencies
import cv2, json, os, skvideo.io, time

cascade_src = 'lp.xml'

# Hybrid mode plate detection
class Hybrid(object):

    # Initialize Hybrid Mode
    def __init__(self, fps=1, res=720, vid_id=1):
        self.FPS = fps
        self.RES = res
        self.VID_ID = vid_id
        self.lp = []
        # Initialize license plate detection
        self.car_cascade = cv2.CascadeClassifier(cascade_src)

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
        k = -1
        frames_count = 0
        for frame in videodata:
            if cv2.waitKey(1) & 0xFF == ord("q"): break
            if not self.lp: break
            k += 1
            if k % skip_frames != 0: continue
            frames_count += 1
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            lps = self.car_cascade.detectMultiScale(image_gray, 1.1, 1)
            if len(lps) != 0:
                cmd = 'curl -X POST'
                j = 0
                for (x, y, w, h) in lps:
                    cv2.imwrite("mode_hybrid/%d.jpg" % j,\
                    image[y-15:y+h+15, x-15:x+w+15])
                    cmd += ' -F image' + str(j) + '=@mode_hybrid/'\
                    + str(j) + '.jpg'
                    j += 1
                cmd += " 'http://ec2-34-211-111-163.us-west-2\
                .compute.amazonaws.com/alpr?n=" + str(j) + "'"
                results = json.loads(os.popen(cmd).read())
                for result in results:
                    i = 0
                    for plate in result["results"]:
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
