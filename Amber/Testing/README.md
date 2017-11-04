# Amber Experiment Script Usage

## Command

python3 run.py "mode" "ip" "perf"
- mode: local or cloud or hybrid
- ip: AWS ip
- perf: 'perf' for performance testing mode

## Output

- Latency: Seconds per analyzed frame
- Bandwidth used (Server side): Total number of bytes sent to cloud

## Building and Running Dockerfile
docker build -t amber-docker .
docker run -ti -e mode=..mode.. -e ip=..ip.. -e perf=..perf..
-v /usr:/usr -v /lib:/lib -v /etc:/etc amber-docker > ..output_file..