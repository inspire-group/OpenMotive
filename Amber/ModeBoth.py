# Import dependencies
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2, json, os, skvideo.io, time

cascade_src = 'lp.xml'

# Raspberry Pi mode plate detection
class ModeBoth(object):

    # Initialize ModeBoth
    def __init__(self, footage = False, color = "Any"):
        self.FPS = 10
        # Initialize camera
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = self.FPS
        self.raw_capture = PiRGBArray(self.camera, size = (640, 480))
        self.cam = not footage
        self.lp = []
        # Initialize license plate detection
        self.car_cascade = cv2.CascadeClassifier(cascade_src)

    # Add license plates to list
    def add(self, plates = []):
        self.lp.extend(plates)

    # Find license plates
    def find(self):
        plates_found = []
        start = time.time()
        if self.cam:
            for frame in self.camera.capture_continuous(self.raw_capture,\
            format = "bgr", use_video_port = True):
                if cv2.waitKey(1) & 0xFF == ord("q"): break
                if not self.lp: break
                image_gray = cv2.cvtColor(frame.array, cv2.COLOR_BGR2GRAY)
                lps = self.car_cascade.detectMultiScale(image_gray, 1.1, 1)
                cmd = 'curl -X POST'
                j = 0
                for (x, y, w, h) in lps:
                    cv2.imwrite("mode_both/%d.jpg" % j,\
                    frame.array[y-15:y+h+15, x-15:x+w+15])
                    cmd += ' -F image' + str(j) + '=@mode_both/'\
                    + str(j) + '.jpg'
                    j += 1
                cmd += " 'http://ec2-54-244-218-121.us-west-2.compute\
                .amazonaws.com/alpr?n=" + str(j) + "'"
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
                                plates_found.append((candidate["plate"],\
                                str(candidate["confidence"])))
                                self.lp.remove(candidate["plate"])
                #cv2.imshow("Both Mode", frame.array)
                self.raw_capture.truncate(0)
            self.camera.close()
        else:
            metadata = skvideo.io.ffprobe('footage.mp4')['video']
            videodata = skvideo.io.vreader('footage.mp4',\
            num_frames = int(metadata['@nb_frames']))
            frame_rate = metadata['@avg_frame_rate'].split('/')
            skip_frames = int(round(int(frame_rate[0]) /\
            int(frame_rate[1]) / self.FPS))
            k = -1
            for frame in videodata:
                if cv2.waitKey(1) & 0xFF == ord("q"): break
                k += 1
                if k % skip_frames != 0: continue
                if not self.lp: break
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                lps = self.car_cascade.detectMultiScale(image_gray, 1.1, 1)
                s = time.time()
                if len(lps) != 0:
                    cmd = 'curl -X POST'
                    j = 0
                    for (x, y, w, h) in lps:
                        cv2.imwrite("mode_both/%d.jpg" % j,\
                        image[y-15:y+h+15, x-15:x+w+15])
                        cmd += ' -F image' + str(j) + '=@mode_both/'\
                        + str(j) + '.jpg'
                        j += 1
                    cmd += " 'http://ec2-54-244-218-121.us-west-2\
                    .compute.amazonaws.com/alpr?n=" + str(j) + "'"
                    results = json.loads(os.popen(cmd).read())
                    print("Time taken for cloud part: %f" % (time.time() - s))
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
                                    plates_found.append((candidate["plate"],\
                                    str(candidate["confidence"])))
                                    self.lp.remove(candidate["plate"])
                                    print("\n\nTime taken: %f" %\
                                    (time.time() - start))
                                    print("Found at video time: %f" %\
                                    (k / skip_frames / self.FPS))
                #cv2.imshow("Both Mode", image)
        cv2.destroyAllWindows()
        return plates_found
