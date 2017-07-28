# AMBER EXPERIMENT SCRIPT USAGE

## COMMAND

python3 run.py "mode" "fps" "resolution" "video_id" "plate1, plate2, plate3, ..."
        - mode: local or cloud or hybrid
        - fps: 1, 5, or 10
        - resolution: 720 or 1080
        - video_id: 1-6

## OUTPUT

Latency ratio: Number of frames analyzed for license plates / second
Bandwidth used (Server side): Total number of bytes sent to cloud