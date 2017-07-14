# Import dependencies
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2, json, os, skvideo.io, time

# Raspberry Pi mode plate detection
class ModeRaspi(object):

    # Initialize camera and OpenALPR
    def __init__(self, footage = False):
        self.FPS = 10
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = self.FPS
        self.raw_capture = PiRGBArray(self.camera, size = (640, 480))
        self.lp = []
        self.cam = not footage
        time.sleep(0.1)

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
                #cv2.imshow("Raspberry Pi Mode", frame.array)
                cv2.imwrite("mode_raspi.jpg", frame.array)
                results = json.loads(os.popen('alpr -j mode_raspi.jpg').read())
                i = 0
                for plate in results["results"]:
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
                self.raw_capture.truncate(0)
            self.camera.close()
        else:
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
                #cv2.imshow("Raspberry Pi Mode", img)
                cv2.imwrite("mode_raspi.jpg", img)
                results = json.loads(os.popen('alpr -j mode_raspi.jpg').read())
                i = 0
                for plate in results["results"]:
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
                            print("\n\nTime taken: %f" % (time.time() - start))
                            print("Found at video time: %f" % (j /\
                            skip_frames / self.FPS))
        cv2.destroyAllWindows()
        return plates_found
